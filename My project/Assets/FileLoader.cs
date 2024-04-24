using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using UnityEditor;


public class FileLoader : MonoBehaviour
{
    string filepath;
    // Start is called before the first frame update
    void Start()
    {
        GameObject testBrain = Resources.Load("TestBrain") as GameObject;
        if (testBrain == null)
        {
            filepath = EditorUtility.OpenFilePanel("Select your scan file", "", "obj");
            Debug.Log(filepath);

            string resourcesPath = Path.Combine(Application.dataPath, "Resources");
            if (!Directory.Exists(resourcesPath))
            {
                Directory.CreateDirectory(resourcesPath);
            }

            string destinationPath = Path.Combine(resourcesPath, Path.GetFileName(filepath));
            File.Move(filepath, destinationPath);

            AssetDatabase.Refresh();
        }
       GameObject brain = Instantiate(Resources.Load("TestBrain"), Vector3.zero, Quaternion.Euler(-90, 0, 0)) as GameObject;


    }
    // Update is called once per frame
    void Update()
    {

    }
}
