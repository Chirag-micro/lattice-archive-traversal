from lattice_archive.models import Actor


def actor_fixtures() -> dict[str, Actor]:
    return {
        "alma": Actor(
            user_id="user-alma",
            workspace_id="ws-finance-a",
            role="member",
            display_name="Alma Chen",
        ),
        "boris": Actor(
            user_id="user-boris",
            workspace_id="ws-finance-a",
            role="ops",
            display_name="Boris Hale",
        ),
        "bria": Actor(
            user_id="user-bria",
            workspace_id="ws-finance-b",
            role="member",
            display_name="Bria Sloan",
        ),
        "nora": Actor(
            user_id="user-nora",
            workspace_id="ws-admin",
            role="admin",
            display_name="Nora Flint",
        ),
    }
