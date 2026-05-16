from lattice_archive.models import Actor, ResolvedBundle


class BundleAccessPolicy:
    def can_access_bundle(self, actor: Actor, bundle: ResolvedBundle) -> bool:
        if bundle.audience == "ops":
            return actor.role in {"ops", "admin"} and actor.workspace_id == bundle.workspace_id
        return actor.workspace_id == bundle.workspace_id or actor.role == "admin"
