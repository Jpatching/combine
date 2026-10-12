# Test audit

Audited baseline `origin/main` (62 Python unittest methods) and integration `8707afc6d111dc4d72316814af37ca3a5559c445` (106 methods: same 62 plus 44). Counts exclude subtests and PowerShell scripts. Read tests and corresponding validation/collection/viewer implementations; no private runtime records used. This is a static audit, not a test execution report.

## Findings

57 baseline tests remain useful. Five become obsolete when the approved lean documentation contract lands: all four HandoffTests and the public-context-staging test. No entire baseline test is a proven duplicate; three tests contain overlapping checks described below. Keep meaningful assertions when consolidating. Parked functionality is retained source, so its correctness tests remain useful; parking alone is no reason to delete.

The four handoff tests currently test rigid format, dates/revisions/PR metadata rather than freshness or consistency. Replace that format contract with a small test of the current issue navigation pointer only if that pointer remains a supported gate. Retain local-link validity and private inventory exclusion; drop staging as a prerequisite to checking a harmless draft document.

## Cleanup result

The cleanup rewrites the five obsolete policy tests: four handoff tests now check
legacy/short pointer acceptance and empty/missing-issue refusal; the staging test
checks that drafts remain unread until tracked, then their links are validated.
All 62 methods remain. The repository gate passes 62 tests on the cleanup branch.

## Every baseline method

### tests/test_doc_links.py

| Method | Class | Reason |
|---|---|---|
| `test_nested_agent_and_research_links_are_checked` | Useful | Uses real Git inventory for nested references. |
| `test_relative_links_fragments_and_spaces_are_accepted` | Useful | Exercises relative paths, fragments and filenames with spaces. |
| `test_angle_bracket_relative_links_with_spaces_and_fragments_are_accepted` | Useful | Exercises bracketed destinations with spaces and fragments. |
| `test_angle_bracket_destination_with_parentheses_is_accepted` | Useful | Exercises parentheses in bracketed destinations. |
| `test_remote_and_anchor_links_are_excluded_with_or_without_brackets` | Useful | Excludes web/email/anchor links consistently. |
| `test_missing_angle_bracket_local_target_is_rejected` | Useful | Rejects bracketed missing local target. |
| `test_angle_bracket_links_to_existing_external_targets_are_rejected` | Useful | Rejects existing outside files through bracketed relative/absolute links. |
| `test_untracked_private_markdown_is_not_read` | Useful | Excludes private/untracked Markdown from scanning. |
| `test_untracked_public_context_is_rejected_until_staged` | Obsolete after cleanup | Enforces staging public context; obsolete under requested relaxed inventory gate. |
| `test_ignored_markdown_under_public_docs_is_not_read` | Useful | Excludes ignored documents even beneath docs. |
| `test_link_outside_repository_is_rejected` | Useful | Rejects repository escape; overlaps external-link invariant but has separate unbracketed parsing path. |

### tests/test_experiences.py

| Method | Class | Reason |
|---|---|---|
| `test_separate_workspaces_do_not_migrate_or_claim_a_build` | Useful | Confirms isolated empty workspace and no invented build/acceptance. |
| `test_repeated_preparation_preserves_local_work` | Useful | Protects user settings from repeated preparation. |
| `test_unknown_id_and_tracked_destination_fail_before_writing` | Useful | Rejects unknown identities and tracked roots before creation. |
| `test_existing_symlink_is_never_followed_or_overwritten` | Useful | Protects symlink targets and refuses existing destinations. |

### tests/test_fortnite_headers.py

| Method | Class | Reason |
|---|---|---|
| `test_v4_has_no_guid_and_index_can_end_at_45_byte_footer` | Useful | Locks actual v4 footer size and inclusive bounds regression. |
| `test_encrypted_flag_is_metadata_only` | Useful | Prevents encrypted index metadata being treated as decrypted content. |
| `test_bad_magic_version_flag_and_truncation` | Useful | Rejects malformed magic/version/flag/truncation. |
| `test_negative_and_overrun_ranges` | Useful | Checks distinct signed and overflow range boundaries. |
| `test_short_file_rejected_even_with_full_buffer` | Useful | Checks declared file length separately from supplied footer bytes. |
| `test_cli_preserves_input_and_existing_report` | Useful | CLI preserves source/report, emits no private path, refuses invalid source. |
| `test_cli_rejects_container_symlink` | Useful | CLI refuses symbolic container links. |

### tests/test_gtaiv_collision.py

| Method | Class | Reason |
|---|---|---|
| `test_command_rejects_invalid_zlib_framing` | Useful | CLI validates checksum, truncation, concatenation and trailing framing. |
| `test_rejects_truncation_and_bad_indices` | Useful | Parser validates short header/bad index; one compressed truncation overlaps framing test. |
| `test_caps_and_unsupported_layouts_refuse_explicitly` | Useful | Checks caps and unsupported layouts, including decompression bound. |
| `test_invalid_faces_coordinates_and_pointer_tags_refuse` | Useful | Checks nonfinite coordinates, repeated vertices, pointer tag and span. |
| `test_command_emits_only_source_safe_verdict_and_refuses_nonfiles` | Useful | CLI success/refusal and FIFO handling; output stays source safe. |
| `test_header_payload_limits_and_invalid_faces_are_bounded` | Useful | Checks input/decompressed bounds, alias spans, degenerate/flagged faces; trailing framing overlaps first test. |
| `test_short_primitive_header_reports_unsupported_before_geometry_span` | Useful | Checks refusal ordering for short unsupported primitive. |
| `test_known_triangle_is_decoded_in_rage_coordinates` | Useful | Checks decoded vertices and face coordinates numerically. |

### tests/test_handoff.py

| Method | Class | Reason |
|---|---|---|
| `test_complete_snapshot_and_explicit_absence_of_pr_are_accepted` | Obsolete after cleanup | Accepts fixed snapshot shape and exact No PR exists phrase. |
| `test_missing_empty_or_duplicate_section_is_rejected` | Obsolete after cleanup | Enforces five exact section headings. |
| `test_missing_empty_or_duplicate_disposition_is_rejected` | Obsolete after cleanup | Enforces duplicate disposition metadata. |
| `test_short_revision_and_missing_tracker_links_are_rejected` | Obsolete after cleanup | Enforces full revision and issue/PR URL forms. |

### tests/test_recipes.py

| Method | Class | Reason |
|---|---|---|
| `test_both_candidates_are_accepted` | Useful | Exercises real pinned candidate fixtures. |
| `test_stale_runtime_commit_is_rejected` | Useful | Rejects source pin drift. |
| `test_wrong_runtime_identity_is_rejected` | Useful | Rejects wrong runtime identity. |
| `test_execution_and_private_path_fields_are_rejected` | Useful | Rejects commands, hooks, private paths and downloads at root. |
| `test_nested_extra_fields_are_rejected` | Useful | Rejects executable extra nested fields. |
| `test_missing_fields_are_rejected` | Useful | Requires complete recipe fields. |
| `test_non_object_roots_are_rejected` | Useful | Rejects JSON roots of wrong types. |
| `test_schema_version_requires_integer_one` | Useful | Rejects boolean/float/string versions, not just wrong integer. |
| `test_invalid_worlds_do_not_crash_validator` | Useful | Rejects unknown and structurally invalid worlds without crashing. |
| `test_world_cannot_omit_additional_content` | Useful | Checks world/content prerequisite relationship. |
| `test_unsupported_modes_are_rejected` | Useful | Rejects unsupported movement and combat. |
| `test_display_control_characters_and_unsafe_ids_are_rejected` | Useful | Checks identifier constraints and display/control text. |
| `test_malformed_duplicate_and_non_finite_json_are_rejected` | Useful | Checks duplicate keys, nonfinite numbers, malformed UTF-8 and excessive depth. |
| `test_size_limit_and_missing_files` | Useful | Checks size boundary and missing-file handling. |
| `test_cli_failure_does_not_echo_untrusted_input` | Useful | CLI errors hide untrusted contents and traceback. |
| `test_cli_runs_outside_repo_without_mutating_recipe` | Useful | CLI works from another cwd and preserves input. |

### tests/test_synergy_diagnostic.py

| Method | Class | Reason |
|---|---|---|
| `test_ordered_flow_and_post_close_shot` | Useful | Accepts complete ordered positive evidence. |
| `test_pre_open_shot_cannot_prove_post_close_firing` | Useful | Rejects firing observation before menu sequence. |
| `test_menu_shot_is_rejected_even_when_flow_completes` | Useful | Rejects menu-open firing despite otherwise complete flow. |
| `test_statistics_only_exempt_with_matching_baseline` | Useful | Permits only known baseline fault and rejects new fault. |
| `test_invalid_baseline_cannot_exempt_statistics` | Useful | Checks baseline build/exit/enable provenance individually. |
| `test_provenance_and_order_required` | Useful | Rejects missing enabled-build and ordered-stream provenance. |
| `test_normal_exit_required` | Useful | Rejects unknown, nonzero and diagnostic-forced exit. |

### tests/test_workbench.py

| Method | Class | Reason |
|---|---|---|
| `test_native_windows_requests_viewer_without_starting_real_apps` | Useful | Windows viewer selection without invoking actual applications. |
| `test_wsl_opens_explicit_media_as_literal_windows_path` | Useful | Literal Windows path quoting prevents shell evaluation. |
| `test_default_opens_comparison_and_print_only_opens_nothing` | Useful | Default viewer and print-only behavior are distinct paths. |
| `test_invalid_batch_opens_nothing` | Useful | Invalid batch is atomic: opens no earlier valid member. |
| `test_viewer_failure_returns_nonzero` | Useful | Viewer invocation failure propagates to CLI exit status. |

## Added integration coverage (44 useful tests)

These are authored/synthetic checks, not evidence of loaded GTA floors or gameplay. Each listed method remains useful for its boundary.

### tests/test_checkpoint.py

2: generated script exercised via Node native shim: movement once, pause/ownership refusal, restoration on collision unavailable; CLI strict data and output preservation. It explicitly leaves loading/layer unqualified.

- `test_authored_checkpoint_native_boundary_moves_once_and_refuses_owned_or_paused_game` — useful.
- `test_checkpoint_preparation_is_strict_data_and_preserves_existing_output` — useful.

### tests/test_evidence_hub.py

8: real HTTP/CLI persistence, request validation/origin, registered immutable media/ranges, missing configuration, stop/reconnect, unchanged-experiment stop and recovery lock. Media fixture is ten bytes, not a playable recording.

- `test_persistent_candidate_and_idempotent_test_request` — useful.
- `test_requests_cannot_supply_commands_or_cross_origin` — useful.
- `test_only_registered_unchanged_media_is_served_with_ranges` — useful.
- `test_missing_runtime_configuration_records_refusal_without_input` — useful.
- `test_stop_pending_batch_survives_reconnect` — useful.
- `test_two_unchanged_failures_stop_and_remain_authored` — useful.
- `test_unverified_recovery_blocks_all_further_requests_from_execution` — useful.
- `test_unchanged_experiment_cannot_restart_in_another_batch` — useful.

### tests/test_gta_workflow.py

5: exclusive runtime operation, explicit hung termination option, redacted missing-config refusal, bounded monitor timeout, idempotent request. These do not execute the Windows launcher/monitor paths.

- `test_recovery_and_diagnostics_cannot_claim_the_runtime_together` — useful.
- `test_hung_termination_is_only_an_explicit_recovery_option` — useful.
- `test_missing_setup_is_named_without_echoing_private_configuration` — useful.
- `test_monitor_rejects_unbounded_wait_before_touching_windows` — useful.
- `test_test_request_is_idempotent_and_missing_setup_is_not_a_game_failure` — useful.

### tests/test_gtaiv_collision.py

11: composite geometry, winding, transform ordering, aggregate caps, child aliases/boxes, precision loss, unsupported child handling and CLI refusal/privacy. Numerical vertex assertions verify behavior rather than implementation shape.

- `test_composite_triangulates_unflagged_quad_without_changing_winding` — useful.
- `test_composite_combines_children_and_bounds_total_output` — useful.
- `test_composite_caps_aggregate_faces_and_rejects_shared_child_buffers` — useful.
- `test_direct_bvh_root_and_quad_rejections` — useful.
- `test_composite_applies_child_rotation_then_translation` — useful.
- `test_composite_refuses_nonfinite_and_nonrigid_transforms` — useful.
- `test_composite_refuses_different_internal_transform` — useful.
- `test_composite_validates_child_boxes_and_all_referenced_spans` — useful.
- `test_composite_rejects_transformed_triangle_precision_loss` — useful.
- `test_composite_refuses_incomplete_or_unsupported_children` — useful.
- `test_composite_command_keeps_geometry_private_and_refuses_whole_resource` — useful.

### tests/test_gtaiv_ground_collection.py

12: collection gate, snapshot freshness/focus, artifacts, restoration/ownership, extra points, retained numeric precision, prepare-only and existing-output preservation. Last test uses external-process shims and is skipped on Windows.

- `test_complete_collection_uses_frozen_gate_and_retains_private_bundle` — useful.
- `test_missing_readings_and_unavailable_queries_remain_inconclusive` — useful.
- `test_stale_status_lost_focus_and_interruption_refuse_collection` — useful.
- `test_artifact_mismatch_refuses_before_observation_execution` — useful.
- `test_restoration_failure_is_visible_even_after_matching_heights` — useful.
- `test_extra_named_points_do_not_change_the_four_point_verdict` — useful.
- `test_additional_points_cannot_be_silently_omitted_from_collection` — useful.
- `test_retained_measurements_preserve_decimal_coordinates_as_numbers` — useful.
- `test_live_collection_refuses_unconfirmed_surface_before_execution` — useful.
- `test_preparation_writes_strict_private_script_without_execution` — useful.
- `test_existing_bundle_is_preserved_even_when_it_has_no_result` — useful.
- `test_retained_observer_blocks_restoration_until_confirmed_exit` — useful.

### tests/test_gtaiv_ground_comparison.py

6: tolerance/stability boundaries, complete qualified point sets, identity matching, disagreement precedence, ambiguous JSON privacy. Qualification is supplied by fixtures; these do not establish a witness.

- `test_all_four_complete_points_agree_at_inclusive_boundaries` — useful.
- `test_unavailable_point_cannot_become_agreement` — useful.
- `test_incomplete_and_unqualified_points_remain_visible` — useful.
- `test_invalid_identity_or_point_set_cannot_silently_replace_fixed_points` — useful.
- `test_stable_disagreement_takes_precedence_over_unavailable_other_point` — useful.
- `test_ambiguous_json_keys_are_rejected_without_private_output` — useful.

## Overlap and missing behavioral coverage

- Collision framing: `test_rejects_truncation_and_bad_indices` repeats compressed truncation already covered by `test_command_rejects_invalid_zlib_framing`; keep its short-header and bad-index assertions. `test_header_payload_limits_and_invalid_faces_are_bounded` repeats trailing-data framing; keep its bounds and face checks. Parser and CLI layers are otherwise distinct.
- Documentation external links: bracketed and unbracketed escape tests repeat the containment invariant but exercise different parsing forms. Consolidation into a parameterized test is optional; it would reduce method count without adding confidence.
- Ground support: no test or retained live evidence here independently identifies which of two stacked floors supports the player. The comparison accepts fixture flags/evidence strings; collection copies witness values from session configuration. Need one reproducible checkpoint with an independently selected floor observation and a deliberately wrong-floor case that fails. Height settling alone is insufficient.
- GTA launcher regression: Python workflow tests never exercise post-response foreground retry, PID/start identity changes, minimized/windowed mode or delayed launcher handoff on Windows. Existing live smoke evidence is separate; a bounded authored Win32 adapter regression would be useful only if this path changes again or live recurrence appears.
- Recording feedback: media serving is tested, automatic capture is not. Missing coverage: trial starts/stops a short recorder owned by that trial; clip is playable/nonempty; measurements and clip refer to the same run/checkpoint/process; recorder failure is visible; cleanup releases the recorder; phone can reach and seek the registered clip. Existing local HTTP hub uses 127.0.0.1 by default; authored serving test proves no phone reachability.
- Baseline gate does not detect stale contradictory task status across README/HANDOFF/issues. Prefer one authoritative current summary and narrow resume pointer over another rigid prose checker.

## Recommendation

Land the cleanup by simplifying the handoff validator and updating its affected tests to the agreed minimal contract. Remove only the obsolete staging policy assertion. Preserve the 57 useful baseline methods and all 44 integration methods. Consolidate overlapping subcases only while touching those suites. Next spend runtime effort on one ground witness plus one short capture and synchronized measurements; add coverage for concrete new behavior, not test count.
