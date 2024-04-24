using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Manipulation : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void ScaleUp()
    {
        transform.localScale += new Vector3(0.25f, 0.25f, 0.25f);
    }

    public void ScaleDown()
    {
        transform.localScale += new Vector3(-0.25f, -0.25f, -0.25f);
    }

    public void RotateLeft()
    {
        transform.Rotate(0, -15, 0);
    }
    public void RotateRight()
    {
        transform.Rotate(0, 15, 0);
    }
}