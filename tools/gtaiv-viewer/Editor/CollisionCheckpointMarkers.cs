using System;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;

namespace CombineQualification
{
    // Temporary visual anchors, never ground queries or qualification verdicts.
    public static class CollisionCheckpointMarkers
    {
        [Serializable] private sealed class Point
        {
            public string label;
            public float[] fixed_world_gta;
        }
        [Serializable] private sealed class PointSet { public Point[] checkpoints; }

        [MenuItem("Combine Qualification/Mark selected collision checkpoints")]
        public static void Mark()
        {
            Material material = null;
            GameObject pending = null;
            try
            {
                if (!CollisionOverlayVisibility.ValidateSelection()) throw new InvalidOperationException();
                string path = Environment.GetEnvironmentVariable("COMBINE_VIEWER_CHECKPOINTS");
                if (string.IsNullOrEmpty(path))
                    path = EditorUtility.OpenFilePanel("Retained private checkpoints", "", "json");
                if (string.IsNullOrEmpty(path)) return;
                if (new FileInfo(path).Length > 32768) throw new InvalidOperationException();
                var input = JsonUtility.FromJson<PointSet>(File.ReadAllText(path));
                if (input?.checkpoints == null || input.checkpoints.Length == 0 ||
                    input.checkpoints.Length > 4) throw new InvalidOperationException();
                var root = Selection.activeGameObject;
                var positions = new List<Vector3>();
                var labels = new HashSet<string>();
                foreach (var point in input.checkpoints)
                {
                    if (point == null || !labels.Add(point.label) ||
                        (point.label != "R1" && point.label != "P1" && point.label != "H1" && point.label != "H2") ||
                        point.fixed_world_gta == null || point.fixed_world_gta.Length != 3)
                        throw new InvalidOperationException();
                    foreach (float value in point.fixed_world_gta)
                        if (float.IsNaN(value) || float.IsInfinity(value)) throw new InvalidOperationException();
                    var position = new Vector3(-point.fixed_world_gta[0], point.fixed_world_gta[2],
                        -point.fixed_world_gta[1]);
                    if (!MatchesCentroid(root, position)) throw new InvalidOperationException();
                    positions.Add(position);
                }
                var shader = Shader.Find("Universal Render Pipeline/Unlit");
                if (shader == null || !shader.isSupported) throw new InvalidOperationException();
                material = new Material(shader) { hideFlags = HideFlags.DontSave };
                material.SetColor("_BaseColor", new Color(1f, 0.35f, 0f));
                pending = new GameObject("Collision checkpoint markers") { hideFlags = HideFlags.DontSave };
                pending.SetActive(false);
                var owner = pending.AddComponent<CollisionCheckpointMarkerRoot>();
                owner.material = material;
                for (int i = 0; i < positions.Count; i++)
                {
                    var anchor = new GameObject(input.checkpoints[i].label) { hideFlags = HideFlags.DontSave };
                    anchor.transform.SetParent(pending.transform, false);
                    anchor.transform.position = positions[i];
                    var line = anchor.AddComponent<LineRenderer>();
                    line.useWorldSpace = false;
                    line.sharedMaterial = material;
                    line.widthMultiplier = 0.08f;
                    line.positionCount = 7;
                    line.SetPositions(new[] {
                        new Vector3(-0.6f, 0.04f, 0), new Vector3(0.6f, 0.04f, 0),
                        new Vector3(0, 0.04f, 0), new Vector3(0, 0.04f, -0.6f),
                        new Vector3(0, 0.04f, 0.6f), new Vector3(0, 0.04f, 0),
                        new Vector3(0, 1.5f, 0)
                    });
                    var label = new GameObject("Label") { hideFlags = HideFlags.DontSave };
                    label.transform.SetParent(anchor.transform, false);
                    label.transform.localPosition = Vector3.up * 1.8f;
                    if (Camera.main != null) label.transform.rotation = Camera.main.transform.rotation;
                    var text = label.AddComponent<TextMesh>();
                    text.text = input.checkpoints[i].label;
                    text.fontSize = 64;
                    text.characterSize = 0.4f;
                    text.anchor = TextAnchor.MiddleCenter;
                    text.color = Color.yellow;
                }
                // Publish only after every point and marker has succeeded.
                ClearExcept(pending);
                pending.SetActive(true);
                pending = null;
                material = null;
                SceneView.RepaintAll();
                Debug.Log("COMBINE_CHECKPOINT_MARKERS: SHOWN (surface/layer and GTA contact unqualified)");
            }
            catch (Exception)
            {
                // Owned paths, JSON, coordinates and exception text stay private.
                if (pending != null) UnityEngine.Object.DestroyImmediate(pending);
                else if (material != null) UnityEngine.Object.DestroyImmediate(material);
                Debug.LogWarning("COMBINE_CHECKPOINT_MARKERS: UNAVAILABLE (selection, point set or scene membership)");
            }
        }

        [MenuItem("Combine Qualification/Clear collision checkpoint markers")]
        public static void Clear() => ClearExcept(null);

        private static void ClearExcept(GameObject preserved)
        {
            // FindObjectsByType excludes DontSave objects. Include our transient,
            // tagged scene roots so cleanup also works after an assembly reload.
            foreach (var owner in Resources.FindObjectsOfTypeAll<CollisionCheckpointMarkerRoot>())
                if (owner.gameObject != preserved && owner.gameObject.scene.IsValid())
                    UnityEngine.Object.DestroyImmediate(owner.gameObject);
        }

        private static bool MatchesCentroid(GameObject root, Vector3 point)
        {
            foreach (var filter in root.GetComponentsInChildren<MeshFilter>())
            {
                var vertices = filter.sharedMesh.vertices;
                var triangles = filter.sharedMesh.triangles;
                for (int i = 0; i < triangles.Length; i += 3)
                {
                    var centroid = (filter.transform.TransformPoint(vertices[triangles[i]]) +
                        filter.transform.TransformPoint(vertices[triangles[i + 1]]) +
                        filter.transform.TransformPoint(vertices[triangles[i + 2]])) / 3f;
                    // Float conversion/import precision only; never move the supplied point.
                    if (Vector3.Distance(centroid, point) <= 0.001f) return true;
                }
            }
            return false;
        }
    }

    internal sealed class CollisionCheckpointMarkerRoot : MonoBehaviour
    {
        public Material material;
        private void OnDestroy()
        {
            if (material != null) DestroyImmediate(material);
        }
    }
}
