import { Card } from "@/components/ui/card";
import { ShieldCheck } from "lucide-react";

export const NoProfilesCard = () => {
  return (
    <Card className="flex w-full flex-col items-center justify-center p-12">
      <ShieldCheck className="mb-4 h-12 w-12 text-muted-foreground" />
      <h3 className="mt-2 text-center">No Active VPN Profiles</h3>
      <p className="mt-2 text-center text-muted-foreground">
        You don't have any active VPN profiles yet. Create one to connect to
        Gaucho Racing's internal network.
      </p>
    </Card>
  );
};

export default NoProfilesCard;
