using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Manipulation : MonoBehaviour
{
    public GameObject globalManager;
    GlobalManager managerScript;
    // Start is called before the first frame update
    void Start()
    {
        GameObject manager = GameObject.FindWithTag("GlobalManager");
        managerScript = manager.GetComponent<GlobalManager>();
    }

    // Update is called once per frame
    void Update()
    {

    }
    public void ScaleUp()
    {
        if (transform.localScale.x <= 1.75f)
        {
            transform.localScale += new Vector3(0.25f, 0.25f, 0.25f);
            foreach (GameObject camera in managerScript.cameras)
            {
                camera.transform.position += new Vector3(0,0,-0.1f);
            }
        }
    }


    public void ScaleDown()
    {
        if (transform.localScale.x > 0.25f)
        {
            transform.localScale += new Vector3(-0.25f, -0.25f, -0.25f);
            foreach (GameObject camera in managerScript.cameras)
            {
                camera.transform.position += new Vector3(0,0,0.1f);
            }
        }
    }

    public void RotateLeft()
    {
        transform.Rotate(0, -15, 0);
    }
    public void RotateRight()
    {
        transform.Rotate(0, 15, 0);
    }
    public void ResetRotation()
    {
         transform.localRotation = Quaternion.identity;
    }

}