1. Only enable strict_mode for OPS bundles by changing the boolean logic.
   This would still leave the validation conditional and doesn't address the fundamental issue that path containment should always be enforced.

2. Block any requested file name containing `..` or starting with `/`.
   Attackers can bypass ad hoc string filters using encoded paths or platform-specific traversal techniques. The core issue is lack of canonical containment validation.

3. Move the audience check into the storage layer.
   The bundle audience check is not the vulnerable step; the path escape remains possible after authorization passes.

4. Remove the strict_mode parameter entirely and always validate.
   This is the correct fix - path validation should never be optional regardless of audience or trust level.
