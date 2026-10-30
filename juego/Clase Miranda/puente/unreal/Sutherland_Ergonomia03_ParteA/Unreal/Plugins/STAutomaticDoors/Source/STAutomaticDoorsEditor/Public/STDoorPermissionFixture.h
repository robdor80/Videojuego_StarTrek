#pragma once
#include "STAutomaticDoor.h"
#include "STDoorPermissionFixture.generated.h"
/** Validation-only adapter. Deliberately overrides the default permission flag. */
UCLASS(Transient,NotPlaceable)
class STAUTOMATICDOORSEDITOR_API ASTDoorPermissionFixture:public ASTAutomaticDoor {
 GENERATED_BODY()
public:
 virtual bool CanActorUseDoor_Implementation(AActor* Requester) const override {return IsValid(Requester);}
};
