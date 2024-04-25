using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SliceToggler : MonoBehaviour
{
    public GameObject ZPlane;
    public GameObject YPlane;
    public GameObject XPlane;


    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

    }
    public void ToggleZPlane()
    {
        ZPlane.SetActive(!ZPlane.activeSelf);
        XPlane.SetActive(false);
        YPlane.SetActive(false);

    }
    public void ToggleYPlane()
    {
        YPlane.SetActive(!YPlane.activeSelf);
        XPlane.SetActive(false);
        ZPlane.SetActive(false);
    }
    public void ToggleXPlane()
    {
        XPlane.SetActive(!XPlane.activeSelf);
        YPlane.SetActive(false);
        ZPlane.SetActive(false);
    }
}
