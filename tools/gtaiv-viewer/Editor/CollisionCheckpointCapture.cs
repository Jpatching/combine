using System;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

namespace CombineQualification
{
    // Inspection views only. Callers establish live loading and resource coverage
    // separately; neither captured pixels nor centroid membership qualify GTA.
    public static class CollisionCheckpointCapture
    {
        private const int Width = 960, Height = 720;

        [MenuItem("Combine Qualification/Capture selected checkpoint views")]
        public static void Capture()
        {
            var selection = Selection.activeGameObject;
            MeshRenderer[] renderers = null;
            bool[] enabled = null;
            var labels = new List<Transform>();
            var rotations = new List<Quaternion>();
            GameObject cameraObject = null;
            RenderTexture target = null;
            Texture2D pixels = null;
            var previousTarget = RenderTexture.active;
            try
            {
                if (!CollisionOverlayVisibility.ValidateSelection()) throw new InvalidOperationException();
                var roots = new List<CollisionCheckpointMarkerRoot>();
                foreach (var root in Resources.FindObjectsOfTypeAll<CollisionCheckpointMarkerRoot>())
                    if (root.gameObject.scene.IsValid() && root.gameObject.activeInHierarchy) roots.Add(root);
                if (roots.Count != 1 || roots[0].transform.childCount < 1 || roots[0].transform.childCount > 4)
                    throw new InvalidOperationException();
                var anchors = new List<Transform>();
                var names = new HashSet<string>();
                foreach (Transform anchor in roots[0].transform)
                {
                    if (!anchor.gameObject.activeInHierarchy || !names.Add(anchor.name) ||
                        (anchor.name != "R1" && anchor.name != "P1" && anchor.name != "H1" && anchor.name != "H2") ||
                        !CollisionCheckpointMarkers.MatchesCentroid(selection, anchor.position)) throw new InvalidOperationException();
                    var text = anchor.GetComponentInChildren<TextMesh>();
                    if (text == null || text.text != anchor.name) throw new InvalidOperationException();
                    anchors.Add(anchor);
                    labels.Add(text.transform);
                    rotations.Add(text.transform.rotation);
                }
                string destination = Environment.GetEnvironmentVariable("COMBINE_VIEWER_CHECKPOINT_CAPTURE");
                if (string.IsNullOrEmpty(destination) || destination.Length > 4096 || !Path.IsPathFullyQualified(destination))
                    throw new InvalidOperationException();
                destination = Path.GetFullPath(destination);
                if (Directory.Exists(destination) || File.Exists(destination) ||
                    Directory.GetParent(destination)?.Exists != true) throw new InvalidOperationException();

                renderers = selection.GetComponentsInChildren<MeshRenderer>(true);
                enabled = new bool[renderers.Length];
                for (int i = 0; i < renderers.Length; i++) enabled[i] = renderers[i].enabled;
                cameraObject = new GameObject("Temporary checkpoint capture camera") {hideFlags = HideFlags.HideAndDontSave};
                var camera = cameraObject.AddComponent<Camera>();
                if (Camera.main != null) camera.CopyFrom(Camera.main);
                camera.enabled = false;
                camera.targetTexture = null;
                camera.clearFlags = CameraClearFlags.SolidColor;
                camera.backgroundColor = new Color(0.03f, 0.03f, 0.03f, 1);
                camera.nearClipPlane = 0.1f;
                camera.farClipPlane = 250;
                camera.aspect = (float)Width / Height;
                camera.orthographic = true;
                camera.orthographicSize = 8;
                var data = cameraObject.AddComponent<UniversalAdditionalCameraData>();
                data.renderType = CameraRenderType.Base;
                data.renderPostProcessing = false;
                target = new RenderTexture(Width, Height, 24) {hideFlags = HideFlags.HideAndDontSave};
                if (!target.Create()) throw new InvalidOperationException();
                pixels = new Texture2D(Width, Height, TextureFormat.RGB24, false) {hideFlags = HideFlags.HideAndDontSave};
                var request = new UniversalRenderPipeline.SingleCameraRequest {destination = target};
                if (!RenderPipeline.SupportsRenderRequest(camera, request)) throw new InvalidOperationException();
                Directory.CreateDirectory(destination);
                foreach (var anchor in anchors)
                foreach (string view in new[] {"oblique", "overhead"})
                {
                    camera.transform.position = anchor.position +
                        (view == "overhead" ? new Vector3(0, 18, 0) : new Vector3(0, 9, -11));
                    if (view == "overhead") camera.transform.rotation = Quaternion.Euler(90, 0, 0);
                    else camera.transform.LookAt(anchor.position);
                    foreach (var label in labels) label.rotation = camera.transform.rotation;
                    // Synchronous pair, identical temporary camera and scene frame.
                    foreach (bool restored in new[] {false, true})
                    {
                        foreach (var renderer in renderers) renderer.enabled = restored;
                        RenderPipeline.SubmitRenderRequest(camera, request);
                        RenderTexture.active = target;
                        pixels.ReadPixels(new Rect(0, 0, Width, Height), 0, 0);
                        pixels.Apply();
                        string file = Path.Combine(destination, anchor.name + "-" + view +
                            (restored ? "-restored.png" : "-map-only.png"));
                        // A conflicting writer can never replace retained evidence.
                        using (var output = new FileStream(file, FileMode.CreateNew, FileAccess.Write))
                        {
                            byte[] png = pixels.EncodeToPNG();
                            output.Write(png, 0, png.Length);
                        }
                    }
                }
                Debug.Log("COMBINE_CHECKPOINT_CAPTURE: WRITTEN (inspection only; surface/layer and GTA contact unqualified)");
            }
            catch (Exception)
            {
                // Partial/refused trials stay visible privately. Paths, coordinates,
                // image contents and exception text are never emitted to the log.
                Debug.LogWarning("COMBINE_CHECKPOINT_CAPTURE: UNAVAILABLE (selection, markers, destination or rendering)");
            }
            finally
            {
                RenderTexture.active = previousTarget;
                if (renderers != null && enabled != null)
                    for (int i = 0; i < renderers.Length; i++)
                        if (renderers[i] != null) renderers[i].enabled = enabled[i];
                for (int i = 0; i < labels.Count; i++) if (labels[i] != null) labels[i].rotation = rotations[i];
                if (pixels != null) UnityEngine.Object.DestroyImmediate(pixels);
                if (target != null) {target.Release(); UnityEngine.Object.DestroyImmediate(target);}
                if (cameraObject != null) UnityEngine.Object.DestroyImmediate(cameraObject);
                Selection.activeGameObject = selection;
            }
        }

    }
}
