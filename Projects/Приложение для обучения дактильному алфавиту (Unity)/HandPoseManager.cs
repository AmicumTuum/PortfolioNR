using System.Collections.Generic;
using UnityEngine;
using TMPro;
using Oculus.Interaction.Input;
using System.IO;
using System.Collections;
using UnityEngine.Networking;
using System;

public class VRHandPoseManager : MonoBehaviour
{
    [SerializeField] private Hand hand;
    [SerializeField] private TextMeshProUGUI feedbackText;
    [SerializeField] private TextMeshProUGUI poseNameText;
    [SerializeField] private SpriteRenderer recognizedSpriteRenderer;
    [SerializeField] private string spriteSheetName = "Dactil"; // имя PNG без расширения
    private Dictionary<int, Sprite> gestureSpritesDict;

    private readonly Dictionary<string, Dictionary<HandJointId, Pose>> savedPoses = new();

    // 33 буквы алфавита
    private readonly List<string> poseNames = new()
    {
        "А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М",
        "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"
    };

    private int currentPoseIndex = 0;

    private readonly HandJointId[] jointsToTrack = new HandJointId[] {
        HandJointId.HandThumb1, HandJointId.HandThumb2, HandJointId.HandThumb3,
        HandJointId.HandIndex0, HandJointId.HandIndex1, HandJointId.HandIndex2, HandJointId.HandIndex3,
        HandJointId.HandMiddle0, HandJointId.HandMiddle1, HandJointId.HandMiddle2, HandJointId.HandMiddle3,
        HandJointId.HandRing0, HandJointId.HandRing1, HandJointId.HandRing2, HandJointId.HandRing3,
        HandJointId.HandPinky0, HandJointId.HandPinky1, HandJointId.HandPinky2, HandJointId.HandPinky3,
        HandJointId.HandWristRoot, HandJointId.HandPalm
    };

    // Сохранение текущего жеста
    public void SaveCurrentPose()
    {
        string poseName = GetCurrentPoseName();
        var pose = new Dictionary<HandJointId, Pose>();

        if (!hand.GetJointPose(HandJointId.HandPalm, out Pose palmPose))
        {
            feedbackText.text = "Не удалось получить позу ладони!";
            return;
        }

        foreach (var joint in jointsToTrack)
        {
            if (hand.GetJointPose(joint, out Pose jointPose))
            {
                Vector3 localPos = Quaternion.Inverse(palmPose.rotation) * (jointPose.position - palmPose.position);
                Quaternion localRot = Quaternion.Inverse(palmPose.rotation) * jointPose.rotation;

                pose[joint] = new Pose(localPos, localRot);
            }
        }

        savedPoses[poseName] = pose;
        feedbackText.text = $"Жест '{poseName}' сохранён!";

        // Сразу записываем жесты в файл
        SavePosesToFile();
    }

    // Сохранение всех жестов в файл
    public void SavePosesToFile()
    {
        string path = Path.Combine(Application.temporaryCachePath, "default_poses_temp.json");

        PoseDataSet poseDataSet = new PoseDataSet { poses = new List<NamedPose>() };

        // Проверка на существующие жесты и перезапись при необходимости
        if (File.Exists(path))
        {
            string json = File.ReadAllText(path);
            poseDataSet = JsonUtility.FromJson<PoseDataSet>(json);
        }

        foreach (var poseEntry in savedPoses)
        {
            NamedPose namedPose = new NamedPose { poseName = poseEntry.Key, joints = new List<JointData>() };

            foreach (var jointEntry in poseEntry.Value)
            {
                JointData jointData = new JointData
                {
                    jointId = jointEntry.Key.ToString(),
                    pose = new PoseData
                    {
                        position = new float[] { jointEntry.Value.position.x, jointEntry.Value.position.y, jointEntry.Value.position.z },
                        rotation = new float[] { jointEntry.Value.rotation.x, jointEntry.Value.rotation.y, jointEntry.Value.rotation.z, jointEntry.Value.rotation.w }
                    }
                };
                namedPose.joints.Add(jointData);
            }

            // Добавить новый жест или перезаписать существующий
            bool isPoseFound = false;
            for (int i = 0; i < poseDataSet.poses.Count; i++)
            {
                if (poseDataSet.poses[i].poseName == namedPose.poseName)
                {
                    poseDataSet.poses[i] = namedPose;
                    isPoseFound = true;
                    break;
                }
            }

            if (!isPoseFound)
            {
                poseDataSet.poses.Add(namedPose);
            }
        }

        // Запись в файл
        string newJson = JsonUtility.ToJson(poseDataSet, true); // true - форматирование
        File.WriteAllText(path, newJson);

        feedbackText.text = "Жесты сохранены в файл!";
    }

    // Получение текущего названия жеста
    public string GetCurrentPoseName()
    {
        return poseNames[currentPoseIndex];
    }

    // Переход к следующему жесту
    public void NextPose()
    {
        currentPoseIndex = (currentPoseIndex + 1) % poseNames.Count;
        UpdatePoseNameDisplay();
    }

    // Переход к предыдущему жесту
    public void PreviousPose()
    {
        currentPoseIndex = (currentPoseIndex - 1 + poseNames.Count) % poseNames.Count;
        UpdatePoseNameDisplay();
    }

    // Сравнение текущего жеста с сохраненным
    public void CompareCurrentPose()
    {
        string poseName = GetCurrentPoseName();

        if (!savedPoses.ContainsKey(poseName))
        {
            feedbackText.text = $"Жест '{poseName}' не сохранён!";
            return;
        }

        if (!hand.GetJointPose(HandJointId.HandPalm, out Pose palmPose))
        {
            feedbackText.text = "Не удалось получить позу ладони!";
            return;
        }

        var saved = savedPoses[poseName];
        float posThreshold = 0.04f;
        float rotThreshold = 25f;

        foreach (var joint in jointsToTrack)
        {
            if (!hand.GetJointPose(joint, out Pose currentPose)) continue;

            Vector3 localPos = Quaternion.Inverse(palmPose.rotation) * (currentPose.position - palmPose.position);
            Quaternion localRot = Quaternion.Inverse(palmPose.rotation) * currentPose.rotation;

            if (!saved.TryGetValue(joint, out Pose savedPose)) continue;

            float posDiff = Vector3.Distance(localPos, savedPose.position);
            float rotDiff = Quaternion.Angle(localRot, savedPose.rotation);

            if (posDiff > posThreshold || rotDiff > rotThreshold)
            {
                feedbackText.text = $"Жест '{poseName}' не совпадает!";
                return;
            }
        }

        feedbackText.text = $"Жест '{poseName}' совпадает!";
    }

    private void LoadPosesFromFile()
    {
        string path = Path.Combine(Application.temporaryCachePath, "default_poses_temp.json");

        if (!File.Exists(path))
        {
            Debug.LogWarning($"Файл не найден: {path}");
            return;
        }

        try
        {
            string json = File.ReadAllText(path);
            PoseDataSet poseDataSet = JsonUtility.FromJson<PoseDataSet>(json);

            if (poseDataSet == null || poseDataSet.poses == null)
            {
                Debug.LogError("Ошибка при разборе JSON — данные пустые или некорректные.");
                return;
            }

            savedPoses.Clear();

            foreach (var namedPose in poseDataSet.poses)
            {
                var jointDict = new Dictionary<HandJointId, Pose>();

                foreach (var jointData in namedPose.joints)
                {
                    if (System.Enum.TryParse(jointData.jointId, out HandJointId jointId))
                    {
                        Vector3 position = new Vector3(jointData.pose.position[0], jointData.pose.position[1], jointData.pose.position[2]);
                        Quaternion rotation = new Quaternion(jointData.pose.rotation[0], jointData.pose.rotation[1], jointData.pose.rotation[2], jointData.pose.rotation[3]);
                        jointDict[jointId] = new Pose(position, rotation);
                    }
                    else
                    {
                        Debug.LogWarning($"Неизвестный сустав: {jointData.jointId}");
                    }
                }

                savedPoses[namedPose.poseName] = jointDict;
            }
            Debug.Log($"Загружено жестов: {savedPoses.Count}");
        }
        catch (Exception ex)
        {
            Debug.LogError($"Ошибка при загрузке файла жестов: {ex.Message}");
        }
    }


    private void Start()
    {
        LoadPosesFromFile();
        UpdatePoseNameDisplay();
    }

    private void Awake()
    {
        LoadSpriteSheet();
    }

    public void SetCurrentPoseIndex(int index)
    {
        currentPoseIndex = index;
        UpdatePoseNameDisplay();
    }

    private void LoadSpriteSheet()
    {
        // Загружаем все спрайты с листа (Multiple) по имени
        gestureSpritesDict = new Dictionary<int, Sprite>();
        var allSprites = Resources.LoadAll<Sprite>(spriteSheetName);

        foreach (var sprite in allSprites)
        {
            // Имена спрайтов вида: Dactil_1, Dactil_2 и т.д.
            string[] parts = sprite.name.Split('_');
            if (parts.Length == 2 && int.TryParse(parts[1], out int index))
            {
                gestureSpritesDict[index] = sprite;
            }
        }
    }

    private void UpdateSpriteByPoseIndex()
    {
        if (recognizedSpriteRenderer == null || gestureSpritesDict == null)
            return;

        int spriteIndex = currentPoseIndex + 1; // т.к. Dactil_1 — это "А", currentPoseIndex = 0

        if (gestureSpritesDict.TryGetValue(spriteIndex, out Sprite sprite))
        {
            recognizedSpriteRenderer.sprite = sprite;
        }
        else
        {
            recognizedSpriteRenderer.sprite = null;
        }
    }


    private void UpdatePoseNameDisplay()
    {
        if (poseNameText != null)
        {
            poseNameText.text = $"Буква: {GetCurrentPoseName()}";
        }

        UpdateSpriteByPoseIndex();
    }

    public Dictionary<HandJointId, Pose> GetCurrentPoseData()
    {
        string poseName = GetCurrentPoseName();
        return savedPoses.ContainsKey(poseName) ? savedPoses[poseName] : null;
    }

}