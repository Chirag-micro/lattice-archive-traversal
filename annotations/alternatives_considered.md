1. Only pass known_entries for all bundle types, not just OPS bundles.
   This would still leave the validation conditional and could break if the heuristic changes in the future. The core issue is that validation should be unconditional.

2. Block any requested file name containing `..` or starting with `/`.
   Attackers can bypass ad hoc string filters using encoded paths or platform-specific traversal techniques. The core issue is lack of canonical containment validation.

3. Move the audience check into the storage layer.
   The bundle audience check is not the vulnerable step; the path escape remains possible after authorization passes.

4. Remove the PathValidator class and use inline validation.
   This would duplicate containment logic and increase the risk of inconsistent validation across code paths.
