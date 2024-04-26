using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GlobalManager : MonoBehaviour
{
    [HideInInspector] public GameObject ZPlane;
    [HideInInspector] public GameObject YPlane;
    [HideInInspector] public GameObject XPlane;
    public GameObject ZPos;
    public GameObject YPos;
    public GameObject XPos;
    [HideInInspector] public GameObject ZCopy;
    [HideInInspector] public GameObject YCopy;
    [HideInInspector] public GameObject XCopy;

    public GameObject[] cameras;
    List<Vector3> cameraPositions = new List<Vector3>();
    // Start is called before the first frame update
    void Start()
    {
        StoreCameraPositions();
    }

    // Update is called once per frame
    void Update()
    {

    }
    public void flush()
    {
        Destroy(ZCopy);
        Destroy(YCopy);
        Destroy(XCopy);
        RestoreCameraPositions();
    }
    void StoreCameraPositions()
    {

        foreach (GameObject camera in cameras)
        {
            Vector3 position = camera.transform.position;
            cameraPositions.Add(position);
        }
    }
    void RestoreCameraPositions()
    {
        for (int i = 0; i < cameras.Length; i++)
        {
            cameras[i].transform.position = cameraPositions[i];
        }
    }
}
