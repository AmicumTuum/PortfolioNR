using System;
using System.Collections.Generic;
using UnityEngine;

[Serializable]
public class PoseDataSet
{
    public List<NamedPose> poses;
}

[Serializable]
public class NamedPose
{
    public string poseName;
    public List<JointData> joints;
}

[Serializable]
public class JointData
{
    public string jointId;
    public PoseData pose;
}

[Serializable]
public class PoseData
{
    public float[] position;
    public float[] rotation;

    public Pose ToPose()
    {
        return new Pose(
            new Vector3(position[0], position[1], position[2]),
            new Quaternion(rotation[0], rotation[1], rotation[2], rotation[3])
        );
    }
}