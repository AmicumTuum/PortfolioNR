using System.Collections.Generic;
using UnityEngine;
using TMPro;
using System.IO;
using Oculus.Interaction.Input;

public class AutoGestureRecognizer : MonoBehaviour
{
    [SerializeField] private Oculus.Interaction.Input.Hand hand;
    [SerializeField] private TextMeshProUGUI feedbackText;
    [SerializeField] private SpriteRenderer recognizedSpriteRenderer;
    [SerializeField] private string spriteSheetName = "Dactil"; // имя без .png

    private Dictionary<string, Dictionary<HandJointId, Pose>> allPoses;

    private readonly HandJointId[] jointsToTrack = new HandJointId[] {
        HandJointId.HandThumb1, HandJointId.HandThumb2, HandJointId.HandThumb3,
        HandJointId.HandIndex0, HandJointId.HandIndex1, HandJointId.HandIndex2, HandJointId.HandIndex3,
        HandJointId.HandMiddle0, HandJointId.HandMiddle1, HandJointId.HandMiddle2, HandJointId.HandMiddle3,
        HandJointId.HandRing0, HandJointId.HandRing1, HandJointId.HandRing2, HandJointId.HandRing3,
        HandJointId.HandPinky0, HandJointId.HandPinky1, HandJointId.HandPinky2, HandJointId.HandPinky3,
        HandJointId.HandWristRoot, HandJointId.HandPalm
    };

    private void Start()
    {
        LoadAllPoses();
        InvokeRepeating(nameof(TryRecognizeGesture), 1f, 1f);
    }

    private void LoadAllPoses()
    {
        allPoses = new Dictionary<string, Dictionary<HandJointId, Pose>>();
        string path = Path.Combine(Application.temporaryCachePath, "default_poses_temp.json");

        if (!File.Exists(path))
        {
            feedbackText.text = "Файл жестов не найден!";
            return;
        }

        string json = File.ReadAllText(path);
        PoseDataSet poseDataSet = JsonUtility.FromJson<PoseDataSet>(json);

        foreach (var namedPose in poseDataSet.poses)
        {
            var jointDict = new Dictionary<HandJointId, Pose>();

            foreach (var jointData in namedPose.joints)
            {
                if (System.Enum.TryParse(jointData.jointId, out HandJointId jointId))
                {
                    Vector3 position = new Vector3(
                        jointData.pose.position[0],
                        jointData.pose.position[1],
                        jointData.pose.position[2]);

                    Quaternion rotation = new Quaternion(
                        jointData.pose.rotation[0],
                        jointData.pose.rotation[1],
                        jointData.pose.rotation[2],
                        jointData.pose.rotation[3]);

                    jointDict[jointId] = new Pose(position, rotation);
                }
            }

            allPoses[namedPose.poseName] = jointDict;
        }
    }

    private int GetPoseIndex(string poseName)
    {
        string[] russianAlphabet = new string[] {
            "А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М",
            "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"
        };

        for (int i = 0; i < russianAlphabet.Length; i++)
        {
            if (russianAlphabet[i] == poseName)
                return i;
        }

        return -1;
    }

    public void TryRecognizeGesture()
    {
        if (allPoses == null || allPoses.Count == 0)
        {
            feedbackText.text = "Жесты не загружены!";
            recognizedSpriteRenderer.sprite = null;
            return;
        }

        if (!hand.GetJointPose(HandJointId.HandPalm, out Pose palmPose))
        {
            feedbackText.text = "Рука не отслеживается!";
            recognizedSpriteRenderer.sprite = null;
            return;
        }

        Dictionary<HandJointId, Pose> currentHand = new();

        foreach (var joint in jointsToTrack)
        {
            if (hand.GetJointPose(joint, out Pose worldPose))
            {
                Vector3 localPos = Quaternion.Inverse(palmPose.rotation) * (worldPose.position - palmPose.position);
                Quaternion localRot = Quaternion.Inverse(palmPose.rotation) * worldPose.rotation;
                currentHand[joint] = new Pose(localPos, localRot);
            }
        }

        float posThreshold = 0.04f;
        float rotThreshold = 25f;

        foreach (var poseEntry in allPoses)
        {
            string poseName = poseEntry.Key;
            var savedPose = poseEntry.Value;
            bool match = true;

            foreach (var joint in jointsToTrack)
            {
                if (!currentHand.TryGetValue(joint, out Pose current)) continue;
                if (!savedPose.TryGetValue(joint, out Pose target)) continue;

                float posDiff = Vector3.Distance(current.position, target.position);
                float rotDiff = Quaternion.Angle(current.rotation, target.rotation);

                if (posDiff > posThreshold || rotDiff > rotThreshold)
                {
                    match = false;
                    break;
                }
            }

            if (match)
            {
                feedbackText.text = $"Показан жест: {poseName}";

                int index = GetPoseIndex(poseName);
                if (index != -1)
                {
                    string targetSpriteName = $"Dactil_{index + 1}";

                    Sprite[] sprites = Resources.LoadAll<Sprite>(spriteSheetName);

                    foreach (var sprite in sprites)
                    {
                        if (sprite.name == targetSpriteName)
                        {
                            recognizedSpriteRenderer.sprite = sprite;
                            return;
                        }
                    }
                }
                recognizedSpriteRenderer.sprite = null;
                return;
            }
        }
        recognizedSpriteRenderer.sprite = null;
        feedbackText.text = "Жест не распознан";
    }
}