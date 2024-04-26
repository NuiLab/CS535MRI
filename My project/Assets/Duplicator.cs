using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UIElements;
using UnityEngine.XR.Interaction.Toolkit;
using UnityVolumeRendering;

public class Duplicator : MonoBehaviour
{
    public GameObject ZPos;
    public GameObject YPos;
    public GameObject XPos;
    public GameObject manager;
    // Start is called before the first frame update
    void Start()
    {
        manager = GameObject.FindWithTag("GlobalManager");
        ZPos = manager.GetComponent<GlobalManager>().ZPos;
        YPos = manager.GetComponent<GlobalManager>().YPos;
        XPos = manager.GetComponent<GlobalManager>().XPos;
    }

    // Update is called once per frame
    void Update()
    {

    }

    public void DuplicateZPlane()
    {
        GameObject ZPlane = GameObject.FindWithTag("ZPlane");
        GameObject newZPlane = Instantiate(ZPlane, ZPlane.transform.position, ZPlane.transform.rotation);
        newZPlane.transform.localScale = ZPlane.transform.lossyScale;
        newZPlane.tag = "Untagged";
        RemoveAllComponentsExceptTransformAndMesh(newZPlane);
        //newZPlane.GetComponent<SlicingPlane>().enabled = false;
        //newZPlane.GetComponent<XRGrabInteractable>().enabled = false;
        //newZPlane.GetComponent<BoxCollider>().enabled = false;
        newZPlane.transform.position = ZPos.transform.position;
        newZPlane.transform.rotation = ZPos.transform.rotation;
        
        if (manager.GetComponent<GlobalManager>().ZCopy == null)
        {
            manager.GetComponent<GlobalManager>().ZCopy = newZPlane;
        }
        else
        {
            Destroy(manager.GetComponent<GlobalManager>().ZCopy);
            manager.GetComponent<GlobalManager>().ZCopy = newZPlane;
        }

    }
    public void DuplicateYPlane()
    {
        GameObject YPlane = GameObject.FindWithTag("YPlane");
        GameObject newYPlane = Instantiate(YPlane, YPlane.transform.position, YPlane.transform.rotation);
        newYPlane.transform.localScale = YPlane.transform.lossyScale;
        newYPlane.tag = "Untagged";
        RemoveAllComponentsExceptTransformAndMesh(newYPlane);
        newYPlane.transform.position = YPos.transform.position;
        newYPlane.transform.rotation = YPos.transform.rotation;
        
        if (manager.GetComponent<GlobalManager>().YCopy == null)
        {
            manager.GetComponent<GlobalManager>().YCopy = newYPlane;
        }
        else
        {
            Destroy(manager.GetComponent<GlobalManager>().YCopy);
            manager.GetComponent<GlobalManager>().YCopy = newYPlane;
        }
    }
    public void DuplicateXPlane()
    {
        GameObject XPlane = GameObject.FindWithTag("XPlane");
        GameObject newXPlane = Instantiate(XPlane, XPlane.transform.position, XPlane.transform.rotation);
        newXPlane.tag = "Untagged";
        newXPlane.transform.localScale = XPlane.transform.lossyScale;
        RemoveAllComponentsExceptTransformAndMesh(newXPlane);
        //newXPlane.GetComponent<SlicingPlane>().enabled = false;
        //newXPlane.GetComponent<XRGrabInteractable>().enabled = false;
        //newXPlane.GetComponent<BoxCollider>().enabled = false;
        newXPlane.transform.position = XPos.transform.position;
        newXPlane.transform.rotation = XPos.transform.rotation;
       
        if (manager.GetComponent<GlobalManager>().XCopy == null)
        {
            manager.GetComponent<GlobalManager>().XCopy = newXPlane;
        }
        else
        {
            Destroy(manager.GetComponent<GlobalManager>().XCopy);
            manager.GetComponent<GlobalManager>().XCopy = newXPlane;
        }
    }
    public void RemoveAllComponentsExceptTransformAndMesh(GameObject obj)
    {
        Destroy(obj.GetComponent<XRGrabInteractable>());
        foreach (var component in obj.GetComponents<Component>())
        {
            if (!(component is Transform || component is MeshFilter || component is MeshRenderer))
            {
                Destroy(component);
            }
        }
    }
}
