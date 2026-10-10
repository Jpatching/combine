using System;
using System.IO;
using System.IO.Compression;
using IVUnity;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using ResourceFile = RageLib.FileSystem.Common.File;

namespace CombineQualification
{
    // Executes the real public viewer path in an empty scene, without a game install.
    public static class CollisionOverlayQualification
    {
        [MenuItem("Combine Qualification/Check authored collision overlay")]
        public static void Run()
        {
            // Interactive callers can have unrelated unsaved scenes open.
            // Cancellation must preserve them and cannot become qualification evidence.
            if (!Application.isBatchMode && !EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo())
            {
                Debug.LogWarning("COMBINE_OVERLAY_QUALIFICATION: UNAVAILABLE (cancelled before scene replacement)");
                return;
            }
            try
            {
                CheckCompleteNonflatOverlay();
                Debug.Log("COMBINE_OVERLAY_QUALIFICATION: PASS (scene geometry; pixels unverified)");
                if (Application.isBatchMode) EditorApplication.Exit(0);
            }
            catch (Exception error)
            {
                Debug.LogException(error);
                Debug.LogError("COMBINE_OVERLAY_QUALIFICATION: FAIL");
                if (Application.isBatchMode) EditorApplication.Exit(1);
                else throw;
            }
        }

        private static void CheckCompleteNonflatOverlay()
        {
            // Never enter Play or open ECSMain: that would start game-file acquisition.
            EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            Require(Shader.Find("Universal Render Pipeline/Lit") != null,
                "Required overlay shader unavailable; cannot qualify output.");
            var parent = new GameObject("Authored overlay qualification");
            var loader = new GTADatLoader("", null);
            byte[] resource = AuthoredComposite();
            loader.gameFiles.Add("authored_nonflat.wbn", new ResourceFile(() => resource));

            CollisionDebugRenderer.RenderAll(loader, parent.transform);

            var renderers = parent.GetComponentsInChildren<MeshRenderer>(true);
            Require(renderers.Length == 2, "Complete resource must produce both child overlays.");
            // Hand-worked values: GTA (12,26,33) becomes Unity (-12,33,-26), etc.
            // These literals are independent of the viewer and Combine's decoder.
            var firstVertices = new[] {
                new Vector3(-12, 33, -26), new Vector3(-18, 30, -17),
                new Vector3(-6, 35, -29)
            };
            var firstFaces = new[] { 0, 2, 1 };
            var secondVertices = new[] {
                new Vector3(40, 10, -50), new Vector3(32, 10, -50),
                new Vector3(32, 14, -53), new Vector3(40, 12, -53)
            };
            var secondFaces = new[] { 0, 2, 1, 0, 3, 2 };
            CheckMesh(renderers[0], firstVertices, firstFaces);
            CheckMesh(renderers[1], secondVertices, secondFaces);

            // Exercise the user-facing commands, retaining the same scene placement.
            var unrelated = new GameObject("Unrelated map renderer").AddComponent<MeshRenderer>();
            Selection.activeGameObject = parent;
            Require(EditorApplication.ExecuteMenuItem("Combine Qualification/Hide selected collision overlay"),
                "Hide overlay command unavailable.");
            foreach (var renderer in renderers)
                Require(!renderer.enabled, "Map-only view still displays a selected overlay child.");
            Require(unrelated.enabled, "Map-only command disabled unrelated geometry.");
            Require(EditorApplication.ExecuteMenuItem("Combine Qualification/Show selected collision overlay"),
                "Show overlay command unavailable.");
            CheckMesh(renderers[0], firstVertices, firstFaces);
            CheckMesh(renderers[1], secondVertices, secondFaces);
            Require(unrelated.enabled, "Restoring the overlay changed unrelated geometry.");

            // Qualification of the selection guard: mixed roots must stay untouched.
            unrelated.transform.SetParent(parent.transform, false);
            Require(!EditorApplication.ExecuteMenuItem("Combine Qualification/Hide selected collision overlay"),
                "A mixed map/overlay root must not enable the visibility command.");
            foreach (var renderer in renderers)
                Require(renderer.enabled, "Refusing a mixed root hid collision geometry.");
            Require(unrelated.enabled, "Refusing a mixed root hid unrelated geometry.");
            unrelated.transform.SetParent(null, false);
            Selection.activeGameObject = null;
            Require(!EditorApplication.ExecuteMenuItem("Combine Qualification/Hide selected collision overlay"),
                "An absent selection must not enable the visibility command.");
            Selection.activeGameObject = parent;

            // Leave the authored scene inspectable after the menu invocation.
            var camera = new GameObject("Authored fixture camera").AddComponent<Camera>();
            camera.transform.position = new Vector3(75, 65, 25);
            camera.transform.LookAt(new Vector3(10, 23, -35));
            camera.nearClipPlane = 0.1f;
            camera.farClipPlane = 250;
            var light = new GameObject("Authored fixture light").AddComponent<Light>();
            light.type = LightType.Directional;
            light.transform.rotation = Quaternion.Euler(50, -30, 0);
            SceneView.RepaintAll();
        }

        private static void CheckMesh(MeshRenderer renderer, Vector3[] expected, int[] triangles)
        {
            Require(renderer.enabled && renderer.gameObject.activeInHierarchy,
                "Overlay is disabled or inactive.");
            Require(renderer.sharedMaterial != null && renderer.sharedMaterial.shader != null &&
                renderer.sharedMaterial.shader.isSupported, "Overlay material unavailable.");
            var filter = renderer.GetComponent<MeshFilter>();
            Require(filter != null && filter.sharedMesh != null, "Overlay mesh missing.");
            var vertices = filter.sharedMesh.vertices;
            Require(vertices.Length == expected.Length, "Overlay vertex count is incomplete.");
            for (int i = 0; i < expected.Length; i++)
            {
                Vector3 observed = filter.transform.TransformPoint(vertices[i]);
                Require(Vector3.Distance(observed, expected[i]) <= 0.0001f,
                    $"Vertex {i}: expected {expected[i]}, observed {observed}.");
            }
            var observedTriangles = filter.sharedMesh.triangles;
            Require(observedTriangles.Length == triangles.Length, "Overlay faces incomplete.");
            for (int i = 0; i < triangles.Length; i++)
                Require(observedTriangles[i] == triangles[i], "Overlay face topology or winding differs.");
        }

        private static void Require(bool condition, string message)
        {
            if (!condition) throw new InvalidOperationException(message);
        }

        private static byte[] AuthoredComposite()
        {
            // Strictly authored RSC5: two geometry children with explicit identity matrices.
            // No bytes, names, coordinates or expectations come from owned game data.
            var system = new byte[0x600];
            using (var stream = new MemoryStream(system))
            using (var writer = new BinaryWriter(stream))
            {
                At(writer, 8); writer.Write(0x50000040u);
                At(writer, 0x44); writer.Write((byte)12);
                BoundBox(writer, 0x40, new Vector3(-40, 17, 10), new Vector3(18, 53, 35));
                At(writer, 0xc0); writer.Write(0x50000100u);
                writer.Write(0x50000120u); writer.Write(0x500001a0u);
                writer.Write(0x50000220u); writer.Write((ushort)2); writer.Write((ushort)2);
                At(writer, 0x100); writer.Write(0x50000280u); writer.Write(0x50000380u);
                for (int matrix = 0; matrix < 4; matrix++)
                {
                    At(writer, 0x120 + matrix * 64);
                    for (int cell = 0; cell < 16; cell++) writer.Write(cell % 5 == 0 ? 1f : 0f);
                }
                At(writer, 0x220);
                Vec(writer, new Vector3(6, 17, 30)); Vec(writer, new Vector3(18, 29, 35));
                Vec(writer, new Vector3(-40, 50, 10)); Vec(writer, new Vector3(-32, 53, 14));
                Geometry(writer, 0x280, 0x480, 0x4c0, 3,
                    new Vector3(2, 3, 0.5f), new Vector3(10, 20, 30));
                Geometry(writer, 0x380, 0x4a0, 0x4e0, 4,
                    new Vector3(1, 0.5f, 2), new Vector3(-40, 50, 10));
                BoundBox(writer, 0x280, new Vector3(6, 17, 30), new Vector3(18, 29, 35));
                BoundBox(writer, 0x380, new Vector3(-40, 50, 10), new Vector3(-32, 53, 14));
                Polygon(writer, 0x480, 0); Polygon(writer, 0x4a0, 3);
                At(writer, 0x4c0);
                foreach (short value in new short[] { 1, 2, 6, 4, -1, 0, -2, 3, 10 }) writer.Write(value);
                At(writer, 0x4e0);
                foreach (short value in new short[] { 0, 0, 0, 8, 0, 0, 8, 6, 2, 0, 6, 1 }) writer.Write(value);
            }
            using var output = new MemoryStream();
            using (var header = new BinaryWriter(output, System.Text.Encoding.UTF8, true))
            {
                header.Write(0x05435352u); header.Write(0x20u);
                header.Write(6u); header.Write((ushort)0xda78);
            }
            using (var compressed = new DeflateStream(output, System.IO.Compression.CompressionLevel.Optimal, true))
                compressed.Write(system, 0, system.Length);
            // 0x78DA in the header begins zlib framing. Complete it with Adler-32,
            // even though the pinned reader consumes raw Deflate after that header.
            uint a = 1, b = 0;
            foreach (byte value in system)
            {
                a = (a + value) % 65521;
                b = (b + a) % 65521;
            }
            uint checksum = (b << 16) | a;
            for (int shift = 24; shift >= 0; shift -= 8)
                output.WriteByte((byte)(checksum >> shift));
            return output.ToArray();
        }

        private static void Geometry(BinaryWriter writer, int offset, int polygon, int vertices,
            int count, Vector3 scale, Vector3 center)
        {
            At(writer, offset + 4); writer.Write((byte)4);
            At(writer, offset + 0x8c); writer.Write(0x50000000u | (uint)polygon);
            Vec(writer, scale); Vec(writer, center);
            writer.Write(0x50000000u | (uint)vertices);
            At(writer, offset + 0xc8); writer.Write(count); writer.Write(1);
        }

        private static void Polygon(BinaryWriter writer, int offset, ushort fourth)
        {
            At(writer, offset); writer.Write(0f); writer.Write(0f); writer.Write(1f); writer.Write(1f);
            writer.Write((ushort)0); writer.Write((ushort)1); writer.Write((ushort)2); writer.Write(fourth);
            for (int i = 0; i < 4; i++) writer.Write((ushort)0xffff);
        }

        private static void Vec(BinaryWriter writer, Vector3 value)
        {
            writer.Write(value.x); writer.Write(value.y); writer.Write(value.z); writer.Write(0f);
        }

        private static void BoundBox(BinaryWriter writer, int offset, Vector3 min, Vector3 max)
        {
            At(writer, offset + 0x10); Vec(writer, max); Vec(writer, min);
        }

        private static void At(BinaryWriter writer, int offset) => writer.BaseStream.Position = offset;
    }
}
