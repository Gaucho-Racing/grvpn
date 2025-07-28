import React from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Client } from "@/models/client";
import { getAxiosErrorMessage } from "@/lib/axios-error-handler";
import { notify } from "@/lib/notify";
import { BACKEND_URL } from "@/consts/config";
import axios from "axios";
import { CopyIcon, DownloadIcon, ExternalLink } from "lucide-react";
import { formatDistanceToNow, isBefore } from "date-fns";
import { Dialog, DialogContent, DialogTitle } from "@/components/ui/dialog";
import { QRCode } from "react-qrcode-logo";
import { DialogTrigger } from "@radix-ui/react-dialog";
import { useUser } from "@/lib/store";

interface ProfileCardProps {
  client: Client;
}

function getRelativeExpiration(date: Date) {
  const now = new Date();
  const expires = new Date(date);
  const isExpired = isBefore(expires, now);
  const distance = formatDistanceToNow(expires, { addSuffix: false });
  return isExpired ? `Expired ${distance} ago` : `Expires in ${distance}`;
}

function getExpirationColor(date: Date) {
  const now = new Date();
  const expires = new Date(date);
  const isExpired = isBefore(expires, now);
  return isExpired
    ? "text-red-500"
    : formatDistanceToNow(expires) < "1 hour"
      ? "text-orange-500"
      : "text-green-500";
}

export const ProfileCard: React.FC<ProfileCardProps> = ({ client }) => {
  const currentUser = useUser();

  const handleDownload = async (id: string) => {
    try {
      const response = await axios.get(
        `${BACKEND_URL}/clients/${id}/download`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("sentinel_access_token")}`,
          },
        },
      );
      const blob = new Blob([response.data], {
        type: "application/octet-stream",
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "grvpn.ovpn";
      a.target = "_blank";
      a.click();
      URL.revokeObjectURL(url);
    } catch (error: any) {
      notify.error(getAxiosErrorMessage(error));
      console.error(error);
    }
  };

  const handleConnect = async (id: string) => {
    const token = `${currentUser.id}-${Date.now()}`;
    const url = `${BACKEND_URL}/clients/${id}/download?token=${token}`;
    console.log(url);
    window.open(`openvpn://import-profile/${url}`, "_blank");
  };

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Card className="cursor-pointer p-2 transition-all duration-200 hover:bg-neutral-900">
          <div className="flex flex-row items-center justify-between">
            <div className="font-mono text-lg">{client.id}</div>
            <div className="flex flex-row items-center gap-2">
              <div
                className={`text-sm ${getExpirationColor(client.expires_at)} px-2`}
              >
                {getRelativeExpiration(client.expires_at)}
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={(e) => {
                  e.stopPropagation();
                  handleDownload(client.id);
                  notify.success("Downloaded profile");
                }}
              >
                <DownloadIcon className="mr-2 h-5 w-5" />
                Download
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={(e) => {
                  e.stopPropagation();
                  handleConnect(client.id);
                }}
              >
                <ExternalLink className="mr-2 h-5 w-5" />
                Connect
              </Button>
            </div>
          </div>
        </Card>
      </DialogTrigger>
      <DialogTitle className="sr-only">VPN Profile Details</DialogTitle>
      <DialogContent className="max-w-2xl">
        <div className="flex flex-row gap-4">
          <div className="">
            <h4>VPN Profile Details</h4>
            <div className="mt-2 font-mono text-lg">{client.id}</div>
            <div className="mt-2">
              <strong>Status:</strong>{" "}
              {isBefore(client.expires_at, new Date()) ? "Expired" : "Active"}
            </div>
            <div className="mt-2">
              <strong>Created At:</strong>{" "}
              {new Date(client.created_at).toLocaleString()}
            </div>
            <div className="mt-2">
              <strong>Expires At:</strong>{" "}
              {new Date(client.expires_at).toLocaleString()}
            </div>
          </div>
          <div className="">
            <QRCode
              value={`${BACKEND_URL}/clients/${client.id}/download?token=${currentUser.id}-${Date.now()}`}
              size={180}
              qrStyle="squares"
              bgColor={"#000000"}
              fgColor={"#ffffff"}
              eyeRadius={5}
              logoImage="/logo/gr-logo-blank.png"
              logoPaddingStyle="circle"
              logoPadding={2}
              logoWidth={50}
              logoHeight={50}
              logoOpacity={1}
            />
          </div>
        </div>
        <div className="">
          <textarea
            className="h-[250px] w-full rounded-md bg-slate-800 p-2 font-mono text-sm"
            value={client.profile_text}
            disabled
          />
        </div>
        <div className="flex flex-row justify-end gap-2">
          <Button
            variant="outline"
            onClick={() => {
              navigator.clipboard.writeText(client.profile_text);
              notify.success("Copied to clipboard");
            }}
          >
            <CopyIcon className="mr-2 h-5 w-5" />
            Copy
          </Button>
          <Button
            variant="outline"
            onClick={() => {
              handleDownload(client.id);
              notify.success("Downloaded profile");
            }}
          >
            <DownloadIcon className="mr-2 h-5 w-5" />
            Download
          </Button>
          <Button
            variant="outline"
            onClick={() => {
              handleConnect(client.id);
            }}
          >
            <ExternalLink className="mr-2 h-5 w-5" />
            Connect
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};
