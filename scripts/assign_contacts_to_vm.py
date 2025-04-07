"""
This script assigns primary & secondary contacts to a
virtual machine using a predetermined contact role
"""

from core.models import ObjectType
from extras.scripts import Script, ObjectVar
from tenancy.choices import ContactPriorityChoices
from tenancy.models import Contact, ContactAssignment, ContactRole
from virtualization.models import VirtualMachine

class AssignContactVM(Script):
    class Meta:
        name = "Assign Contacts to VM"
        description = "Takes a primary & secondary owner and assigns them to an existing VM"
        scheduling_enabled = False

    # Main form
    primary_owner = ObjectVar(label="Primary Owner", model=Contact)
    secondary_owner = ObjectVar(label="Secondary Owner", model=Contact)
    vm = ObjectVar(label="Virtual Machine", model=VirtualMachine)

    def run(self, data, commit):

        # Get VM object type & owner role. Owner role must exist.
        vm_object_type = ObjectType.objects.get(model='virtualmachine')
        contact_owner_role = ContactRole.objects.get(slug="owner")

        # Create contact assignments
        ownerPrimary = ContactAssignment(
            object_type=vm_object_type,
            object_id=data["vm"].id,
            contact=data["primary_owner"],
            role=contact_owner_role,
            priority=ContactPriorityChoices.PRIORITY_PRIMARY,
        )
        ownerPrimary.full_clean()
        ownerPrimary.save()

        ownerSecondary = ContactAssignment(
            object_type=vm_object_type,
            object_id=data["vm"].id,
            contact=data["secondary_owner"],
            role=contact_owner_role,
            priority=ContactPriorityChoices.PRIORITY_SECONDARY,
        )
        ownerSecondary.full_clean()
        ownerSecondary.save()

        self.log_success(f"Successfully assigned contacts {ownerPrimary.contact.name} & {ownerSecondary.contact.name} to {data['vm'].name}.")
