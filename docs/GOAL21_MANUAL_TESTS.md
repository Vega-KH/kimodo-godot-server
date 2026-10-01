# Goal 21 — final Stage 1 manual acceptance

Completed acceptance record: the user passed all five checks on 2026-10-01.
Goal 21 and Stage 1 are complete. The walkthrough used the normal project or prepared
clean project at `C:/code/godot-kimodo/stage1-clean-project/project.godot`.
Its add-on is installed, Jenny04 was freshly imported, and **Clean install live
smoke** has one one-take generation and one two-take generation (three drafts).
Its `exports/` folder contains all four Save types and a production library.
These are disposable internal test assets, not distributed fixtures.

1. **Preview and normal authoring.** Open that session and select a History take,
   then connect to the backend started with `kimodo-godot-server/start.bat`.
   Generate one/two takes if desired. Check the square viewport at narrow and
   wider dock sizes, take switching, camera following/orbit, Play/Loop/scrubbing,
   and access to Save/Accept. Extra height should scroll vertically, not clip
   buttons horizontally. Stop waiting must not claim to cancel backend inference.
2. **Independent output and Undo.** Save a character animation using a new name;
   optionally save a Character Preview. Accept a named clip into the existing
   `exports/production.res`, Undo and Redo. Verify it on a fresh imported Jenny04
   using an AnimationPlayer rooted at the character root. A character library
   uses that character's bone paths; the humanoid library targets the humanoid
   intermediate, not Jenny. Type a new prompt before Undo and confirm it survives.
3. **Restart/offline recovery.** Stop the backend, restart Godot, reopen the
   session and load History. The character preview should rebuild without HTTP.
   Optionally temporarily rename one managed take `.res` outside the editor:
   reopen the session and check its missing-archive explanation; restore the
   filename and reopen again. Do not rename/delete your independent saved outputs.
   Missing data must not be invented or silently regenerated.
4. **Counted session deletion.** Create enough disposable named sessions to
   exceed eight; the chooser should still list the older ones. Select a session
   with multiple source takes, press Delete…, and confirm the count/preservation
   text. For the prepared smoke session the initial count is three, unless you
   generated/deleted additional takes. Cancel once, then confirm deletion.
   Only its session file and managed data should disappear; other sessions,
   explicit exports, production libraries and shared rig profiles remain usable.
   Try Undo and restart: the deleted session must not reappear. Library Undo is
   still independent. A tiny identity/recovery receipt intentionally remains.
5. **Empty/active session deletion.** Open a disposable empty session and use its
   active Delete… button. Expect a zero-draft warning and, after confirmation,
   return to the chooser with authoring controls hidden. During generation,
   switching/deleting sessions is disabled until generation finishes or you
   choose Stop waiting.

Please report any failure before we mark Goal 21 complete. Destructive-edge
tests (duplicate UUIDs, reserved outputs, stale confirmation, real Windows
junction/file locks and interrupted staging/cleanup) already run automatically;
you do not need to recreate those filesystem fixtures manually.
