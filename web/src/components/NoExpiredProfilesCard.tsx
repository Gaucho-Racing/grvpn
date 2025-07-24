import { Card } from "@/components/ui/card";
import { ShieldX } from "lucide-react";

export const NoExpiredProfilesCard = () => {
  return (
    <Card className="flex w-full flex-col items-center justify-center p-12">
      <ShieldX className="mb-4 h-12 w-12 text-muted-foreground" />
      <h3 className="mt-2 text-center">No Expired VPN Profiles</h3>
      <p className="mt-2 text-center text-muted-foreground">
        VPN profiles expire after 8 hours by default. You will see them listed
        here.
      </p>
    </Card>
  );
};

export default NoExpiredProfilesCard;
