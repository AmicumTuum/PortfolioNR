using System.Collections.Generic;
using UnityEngine;
using Oculus.Interaction.Input;

public class StaticHandVisualizer : MonoBehaviour
{
    public Dictionary<HandJointId, Pose> poseData;

    [Header("Визуальные параметры")]
    public float boneSize = 0.01f;
    public Material jointMaterial;
    public Material lineMaterial;

    private Dictionary<HandJointId, GameObject> jointVisuals = new();
    private List<LineRenderer> boneLines = new();

    public void ShowPose(Dictionary<HandJointId, Pose> pose)
    {
        ClearPrevious(); // если нужно обновить визуализацию

        poseData = pose;

        foreach (var joint in pose)
        {
            GameObject sphere = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            sphere.transform.parent = this.transform;
            sphere.transform.localPosition = joint.Value.position;
            sphere.transform.localRotation = joint.Value.rotation;
            sphere.transform.localScale = Vector3.one * boneSize;

            if (jointMaterial != null)
                sphere.GetComponent<Renderer>().material = jointMaterial;

            jointVisuals[joint.Key] = sphere;
        }

        DrawBones();
    }

    private void DrawBones()
    {
        // Примеры соединений (можно расширить вручную)
        Connect(HandJointId.HandWristRoot, HandJointId.HandPalm);
        Connect(HandJointId.HandPalm, HandJointId.HandIndex0);
        Connect(HandJointId.HandIndex0, HandJointId.HandIndex1);
        Connect(HandJointId.HandIndex1, HandJointId.HandIndex2);
        Connect(HandJointId.HandIndex2, HandJointId.HandIndex3);

        Connect(HandJointId.HandPalm, HandJointId.HandMiddle0);
        Connect(HandJointId.HandMiddle0, HandJointId.HandMiddle1);
        Connect(HandJointId.HandMiddle1, HandJointId.HandMiddle2);
        Connect(HandJointId.HandMiddle2, HandJointId.HandMiddle3);

        Connect(HandJointId.HandPalm, HandJointId.HandRing0);
        Connect(HandJointId.HandRing0, HandJointId.HandRing1);
        Connect(HandJointId.HandRing1, HandJointId.HandRing2);
        Connect(HandJointId.HandRing2, HandJointId.HandRing3);

        Connect(HandJointId.HandPalm, HandJointId.HandPinky0);
        Connect(HandJointId.HandPinky0, HandJointId.HandPinky1);
        Connect(HandJointId.HandPinky1, HandJointId.HandPinky2);
        Connect(HandJointId.HandPinky2, HandJointId.HandPinky3);

        Connect(HandJointId.HandPalm, HandJointId.HandThumb1);
        Connect(HandJointId.HandThumb1, HandJointId.HandThumb2);
        Connect(HandJointId.HandThumb2, HandJointId.HandThumb3);
    }

    private void Connect(HandJointId a, HandJointId b)
    {
        if (!jointVisuals.ContainsKey(a) || !jointVisuals.ContainsKey(b))
            return;

        GameObject lineObj = new GameObject($"Line_{a}_{b}");
        lineObj.transform.parent = this.transform;

        LineRenderer lr = lineObj.AddComponent<LineRenderer>();
        lr.positionCount = 2;
        lr.SetPosition(0, jointVisuals[a].transform.localPosition);
        lr.SetPosition(1, jointVisuals[b].transform.localPosition);
        lr.startWidth = 0.002f;
        lr.endWidth = 0.002f;
        lr.material = lineMaterial;

        boneLines.Add(lr);
    }

    private void ClearPrevious()
    {
        foreach (var go in jointVisuals.Values)
        {
            Destroy(go);
        }

        foreach (var line in boneLines)
        {
            Destroy(line.gameObject);
        }

        jointVisuals.Clear();
        boneLines.Clear();
    }
}
