using System;
using System.IO;
using System.IO.Compression;
using System.Linq;
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
                Debug.Log("COMBINE_OVERLAY_QUALIFICATION: PASS (authored geometry, checkpoint pairs and cleanup)");
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

            // The public checkpoint command must anchor markers to unchanged resource
            // geometry. These literal centroids were worked from the authored shapes.
            string checkpointFile = Path.GetTempFileName();
            string priorFile = Environment.GetEnvironmentVariable("COMBINE_VIEWER_CHECKPOINTS");
            try
            {
                File.WriteAllText(checkpointFile,
                    "{\"checkpoints\":[{\"label\":\"R1\",\"fixed_world_gta\":[12,24,32.6666667]}," +
                    "{\"label\":\"P1\",\"fixed_world_gta\":[-34.6666667,51,11.3333333]}]}");
                Environment.SetEnvironmentVariable("COMBINE_VIEWER_CHECKPOINTS", checkpointFile);
                Require(EditorApplication.ExecuteMenuItem("Combine Qualification/Mark selected collision checkpoints"),
                    "Checkpoint marker command unavailable.");
                var markers = GameObject.Find("Collision checkpoint markers");
                Require(markers != null && markers.transform.childCount == 2,
                    "Complete checkpoint markers missing.");
                Require(Vector3.Distance(markers.transform.Find("R1").position,
                    new Vector3(-12, 32.6666667f, -24)) < 0.0001f, "Road marker misplaced.");
                Require(Vector3.Distance(markers.transform.Find("P1").position,
                    new Vector3(34.6666667f, 11.3333333f, -51)) < 0.0001f, "Pavement marker misplaced.");
                Require(markers.GetComponentsInChildren<Collider>().Length == 0,
                    "Inspection markers must not introduce physical contact.");
                CheckMesh(renderers[0], firstVertices, firstFaces);
                CheckMesh(renderers[1], secondVertices, secondFaces);
                Require(unrelated.enabled, "Checkpoint command changed unrelated rendering.");
                CheckCheckpointCapture(parent, renderers, markers);
                File.WriteAllText(checkpointFile,
                    "{\"checkpoints\":[{\"label\":\"R1\",\"fixed_world_gta\":[12,24,32.6666667]}," +
                    "{\"label\":\"P1\",\"fixed_world_gta\":[0,0,0]}]}");
                Require(EditorApplication.ExecuteMenuItem("Combine Qualification/Mark selected collision checkpoints"),
                    "Checkpoint refusal command unavailable.");
                Require(GameObject.Find("Collision checkpoint markers") == markers &&
                    markers.transform.childCount == 2, "Refused point set replaced retained markers.");
                Require(EditorApplication.ExecuteMenuItem("Combine Qualification/Clear collision checkpoint markers"),
                    "Marker clearing command unavailable.");
                Require(GameObject.Find("Collision checkpoint markers") == null,
                    "Temporary marker clearing left scene objects.");
            }
            finally
            {
                Environment.SetEnvironmentVariable("COMBINE_VIEWER_CHECKPOINTS", priorFile);
                File.Delete(checkpointFile);
            }

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

        private static void CheckCheckpointCapture(GameObject parent, MeshRenderer[] renderers,
            GameObject markers)
        {
            string destination = Path.Combine(Path.GetTempPath(), "combine-authored-capture-" + Guid.NewGuid().ToString("N"));
            string prior = Environment.GetEnvironmentVariable("COMBINE_VIEWER_CHECKPOINT_CAPTURE");
            var originalCamera = new GameObject("Capture preservation camera").AddComponent<Camera>();
            originalCamera.tag = "MainCamera";
            originalCamera.transform.position = new Vector3(75, 65, 25);
            originalCamera.transform.rotation = Quaternion.Euler(30, 15, 0);
            originalCamera.fieldOfView = 47;
            var fixtureLight = new GameObject("Capture fixture light").AddComponent<Light>();
            fixtureLight.type = LightType.Directional;
            fixtureLight.transform.rotation = Quaternion.Euler(50, -30, 0);
            var camerasBefore = Resources.FindObjectsOfTypeAll<Camera>().Where(c => c.gameObject.scene.IsValid()).ToArray();
            var labels = markers.GetComponentsInChildren<TextMesh>();
            var labelRotations = labels.Select(label => label.transform.rotation).ToArray();
            try
            {
                Environment.SetEnvironmentVariable("COMBINE_VIEWER_CHECKPOINT_CAPTURE", destination);
                Require(EditorApplication.ExecuteMenuItem("Combine Qualification/Capture selected checkpoint views"),
                    "Checkpoint capture command unavailable.");
                Require(Directory.Exists(destination) && Directory.GetFiles(destination, "*.png").Length == 8,
                    "Both complete checkpoint view pairs must be written.");
                foreach (string label in new[] { "R1", "P1" })
                foreach (string view in new[] { "oblique", "overhead" })
                {
                    var map = new Texture2D(2, 2);
                    var overlay = new Texture2D(2, 2);
                    try
                    {
                        Require(map.LoadImage(File.ReadAllBytes(Path.Combine(destination, label + "-" + view + "-map-only.png"))) &&
                            overlay.LoadImage(File.ReadAllBytes(Path.Combine(destination, label + "-" + view + "-restored.png"))),
                            "Checkpoint view images unavailable.");
                        Require(map.width == 960 && map.height == 720 && overlay.width == 960 && overlay.height == 720,
                            "Checkpoint view dimensions differ.");
                        var before = map.GetPixels32();
                        var after = overlay.GetPixels32();
                        int different = 0;
                        int anchor = 0;
                        for (int i = 0; i < before.Length; i++)
                        {
                            if (Math.Abs(before[i].r - after[i].r) + Math.Abs(before[i].g - after[i].g) +
                                Math.Abs(before[i].b - after[i].b) > 20) different++;
                            // Orange anchor strokes in the middle third prove the base
                            // stayed framed; the authored mesh supplies the pair difference.
                            int x = i % map.width, y = i / map.width;
                            if (x > 320 && x < 640 && y > 240 && y < 480 &&
                                before[i].r > 140 && before[i].g > 35 && before[i].g < 180 && before[i].b < 80)
                                anchor++;
                        }
                        Require(different > 100, "Restored image has no meaningful authored overlay pixels.");
                        Require(anchor > 5, "Checkpoint base is not visible near the view center.");
                    }
                    finally { UnityEngine.Object.DestroyImmediate(map); UnityEngine.Object.DestroyImmediate(overlay); }
                }
                Require(Selection.activeGameObject == parent && GameObject.Find("Collision checkpoint markers") == markers,
                    "Capture changed the selected root or marker set.");
                foreach (var renderer in renderers) Require(renderer.enabled, "Capture failed to restore overlay visibility.");
                Require(originalCamera.transform.position == new Vector3(75, 65, 25) &&
                    Quaternion.Angle(originalCamera.transform.rotation, Quaternion.Euler(30, 15, 0)) < 0.001f &&
                    originalCamera.fieldOfView == 47 && originalCamera.enabled,
                    "Capture changed the original camera.");
                Require(Resources.FindObjectsOfTypeAll<Camera>().Count(c => c.gameObject.scene.IsValid()) == camerasBefore.Length,
                    "Capture leaked a temporary camera.");
                for (int i = 0; i < labels.Length; i++) Require(labels[i].transform.rotation == labelRotations[i],
                    "Capture changed a retained marker label orientation.");
                Require(Vector3.Distance(markers.transform.Find("R1").position,
                    new Vector3(-12, 32.6666667f, -24)) < 0.0001f &&
                    Vector3.Distance(markers.transform.Find("P1").position,
                    new Vector3(34.6666667f, 11.3333333f, -51)) < 0.0001f,
                    "Capture moved retained checkpoint anchors.");
                CheckMesh(renderers[0], new[] {new Vector3(-12, 33, -26), new Vector3(-18, 30, -17),
                    new Vector3(-6, 35, -29)}, new[] {0, 2, 1});
                CheckMesh(renderers[1], new[] {new Vector3(40, 10, -50), new Vector3(32, 10, -50),
                    new Vector3(32, 14, -53), new Vector3(40, 12, -53)}, new[] {0, 2, 1, 0, 3, 2});

                // Existing output is evidence, including failed takes: refusal must
                // preserve it and the prior partially hidden overlay state.
                var files = Directory.GetFiles(destination).OrderBy(file => file).ToArray();
                var contents = files.Select(File.ReadAllBytes).ToArray();
                renderers[0].enabled = false;
                Require(EditorApplication.ExecuteMenuItem("Combine Qualification/Capture selected checkpoint views"),
                    "Capture refusal command unavailable.");
                Require(Directory.GetFiles(destination).Length == files.Length,
                    "Refused capture changed retained output files.");
                for (int i = 0; i < files.Length; i++) Require(contents[i].SequenceEqual(File.ReadAllBytes(files[i])),
                    "Refused capture replaced retained evidence.");
                Require(!renderers[0].enabled && renderers[1].enabled && Selection.activeGameObject == parent,
                    "Refused capture changed visibility or selection.");
                renderers[0].enabled = true;
            }
            finally
            {
                Environment.SetEnvironmentVariable("COMBINE_VIEWER_CHECKPOINT_CAPTURE", prior);
                if (Directory.Exists(destination)) Directory.Delete(destination, true);
                UnityEngine.Object.DestroyImmediate(originalCamera.gameObject);
                UnityEngine.Object.DestroyImmediate(fixtureLight.gameObject);
            }
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
