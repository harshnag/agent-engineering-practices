# The deployment trust boundary

Read `SKILL.md` first. This is the design for keeping production authority away
from code that has not passed review.

## Threat model

Pull request code may execute during tests and builds. If that environment also
holds production credentials, the branch can use them regardless of whether the
official deploy step is conditional.

The threat is not necessarily malicious code. A misconfigured script, postinstall
hook, diagnostic, or target flag has the same authority.

## Build and attest

The gated environment:

1. checks out the exact trunk revision;
2. builds every deployable component once;
3. records a manifest of paths, digests, build identity, and intended target;
4. signs or otherwise protects the manifest from later artifact edits;
5. publishes the artifact without production credentials.

Rebuilding in the deploy environment creates a second unreviewed subject. The
artifact that passed is the artifact that ships.

## Upload without executing the artifact

The deployment environment:

- accepts only artifacts from the gated channel;
- installs no dependencies from them;
- runs no artifact-supplied scripts;
- checks every digest;
- compares target and configuration against host-held policy;
- uploads;
- verifies running identity and user-reachable bytes.

The policy cannot live solely inside the artifact it constrains.

## Controls to prove

- An untrusted-branch job cannot select the deploy environment.
- No untrusted-branch environment holds the production credential.
- A digest mismatch stops before upload.
- A target mismatch stops before upload.
- A dry run starts no upload-capable child.
- An upload success with wrong running identity is still a failure.
- Adding a newly eligible host cannot silently widen credential reach.

Each control is mutation-tested separately. A sabotage that fails everything
only proves the pipeline is broken.
