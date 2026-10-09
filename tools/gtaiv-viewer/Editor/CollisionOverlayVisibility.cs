using System;
using UnityEditor;
using UnityEngine;

namespace CombineQualification
{
    // Inspection only: the selected root must contain collision renderers exclusively.
    public static class CollisionOverlayVisibility
    {
        private const string HideMenu = "Combine Qualification/Hide selected collision overlay";
        private const string ShowMenu = "Combine Qualification/Show selected collision overlay";

        [MenuItem(HideMenu)]
        public static void Hide() => SetVisible(false);

        [MenuItem(ShowMenu)]
        public static void Show() => SetVisible(true);

        [MenuItem(HideMenu, true)]
        [MenuItem(ShowMenu, true)]
        public static bool ValidateSelection() => SelectedOverlay() != null;

        private static MeshRenderer[] SelectedOverlay()
        {
            var selected = Selection.activeGameObject;
            if (selected == null || !selected.activeInHierarchy) return null;
            var renderers = selected.GetComponentsInChildren<MeshRenderer>(true);
            if (renderers.Length == 0) return null;
            foreach (var renderer in renderers)
            {
                // This naming contract belongs to the pinned CollisionDebugRenderer.
                var filter = renderer.GetComponent<MeshFilter>();
                if (!renderer.name.StartsWith("col_", StringComparison.Ordinal) ||
                    !renderer.gameObject.activeInHierarchy || filter == null ||
                    filter.sharedMesh == null || filter.sharedMesh.vertexCount == 0)
                    return null;
            }
            return renderers;
        }

        private static void SetVisible(bool visible)
        {
            var renderers = SelectedOverlay();
            if (renderers == null)
            {
                Debug.LogWarning("COMBINE_OVERLAY_VISIBILITY: UNAVAILABLE (select a collision-only root)");
                return;
            }
            if (!Application.isPlaying) Undo.RecordObjects(renderers, "Collision overlay visibility");
            foreach (var renderer in renderers) renderer.enabled = visible;
            SceneView.RepaintAll();
            Debug.Log(visible ? "COMBINE_OVERLAY_VISIBILITY: SHOWN" : "COMBINE_OVERLAY_VISIBILITY: HIDDEN");
        }
    }
}
