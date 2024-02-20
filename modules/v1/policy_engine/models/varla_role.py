from __future__ import annotations

from functools import cached_property
from typing import List

from pydantic import BaseModel, computed_field
from . import VarlaPolicyBundle, VarlaPolicy


class VarlaRole(BaseModel):
    """VarlaPolicy is a base class that represents the policies that are used in the system."""

    bundles: List[VarlaPolicyBundle]

    @computed_field
    @cached_property
    def policies_bundles(self) -> dict[str, int]:
        return {bundle.type: bundle.policies_bundle for bundle in self.bundles}

    def hasAccessTo(self, policy: VarlaPolicy) -> bool:
        return (
            self.policies_bundles[policy.__objclass__.__name__] & policy.value
        ) == policy.value

    def __add__(self, other: VarlaRole) -> VarlaRole:
        bundles = {bundle.type: bundle.model_copy() for bundle in self.bundles}
        other_bundles = [bundle.model_copy() for bundle in other.bundles]

        for bundle in other_bundles:
            if bundle.type in bundles:
                bundles[bundle.type] = bundles[bundle.type] + bundle
            else:
                bundles[bundle.type] = bundle

        return VarlaRole(bundles=bundles.values())


# Example of a role class

# class UserRole:
#     Normal = VarlaRole(
#         bundles=[
#             VarlaPolicyBundle[AuthenticationPolicy](
#                 policies=[
#                     AuthenticationPolicy.canLogin,
#                 ]
#             )
#         ]
#     )

#     Admin = (
#         VarlaRole(
#             bundles=[
#                 VarlaPolicyBundle[AuthenticationPolicy](
#                     policies=[
#                         AuthenticationPolicy.canResetPassword,
#                     ]
#                 ),
#             ]
#         )
#         + Normal
#     )

#     SuperAdmin = (
#         VarlaRole(
#             bundles=[
#                 VarlaPolicyBundle[AuthenticationPolicy](
#                     policies=[
#                         AuthenticationPolicy.all,
#                     ]
#                 ),
#             ]
#         )
#         + Admin
#     )
