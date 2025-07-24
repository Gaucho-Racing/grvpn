import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useNavigate } from "react-router-dom";
import { logout } from "@/lib/auth";
import { useUser } from "@/lib/store";
import { BACKEND_URL } from "@/consts/config";
import axios from "axios";
import { notify } from "@/lib/notify";
import { getAxiosErrorMessage } from "@/lib/axios-error-handler";
import React, { useState } from "react";
import { Card } from "@/components/ui/card";

interface HeaderProps {
  className?: string;
  style?: React.CSSProperties;
}

const Header = (props: HeaderProps) => {
  const navigate = useNavigate();
  const currentUser = useUser();

  const [connected, setConnected] = useState({ connected: false, ip: "" });

  React.useEffect(() => {
    const interval = setInterval(checkConnection, 2000);
    return () => clearInterval(interval);
  }, []);

  const checkConnection = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/test`);
      setConnected(response.data);
    } catch (error: any) {
      notify.error(getAxiosErrorMessage(error));
      console.error(error);
    }
  };

  return (
    <div
      className={`w-full items-center justify-start border-b border-neutral-800 transition-all duration-200 lg:pl-32 lg:pr-32 ${props.className}`}
      style={{ ...props.style }}
    >
      <div className="flex flex-row items-center justify-between">
        <div className="flex flex-row items-center p-4">
          <img src="/logo/grvpn.png" width={50} height={50} alt="Logo" />
          <h1 className="ml-4">grvpn</h1>
        </div>
        <div className="mr-4 flex flex-row items-center p-4">
          <Card className="mx-4 flex flex-row items-center justify-center gap-4 px-4">
            {connected.connected ? (
              <div className="h-4 w-4 rounded-full bg-green-500" />
            ) : (
              <div className="h-4 w-4 rounded-full bg-red-500" />
            )}
            <div className="flex flex-col items-start">
              {connected.connected ? (
                <div>Connected</div>
              ) : (
                <div>Disconnected</div>
              )}
              <div className="text-gray-400">IP: {connected.ip}</div>
            </div>
          </Card>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Avatar className="cursor-pointer">
                <AvatarImage src={currentUser.avatar_url} />
                <AvatarFallback>CN</AvatarFallback>
              </Avatar>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="mt-2 w-56" align="end">
              <DropdownMenuItem>
                <div className="flex flex-col">
                  <p>
                    {currentUser.first_name} {currentUser.last_name}
                  </p>
                  <p className="text-gray-400">{currentUser.email}</p>
                </div>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() =>
                  window.open(
                    "https://sso.gauchoracing.com/users/348220961155448833/edit",
                    "_blank",
                  )
                }
              >
                <div className="flex">Profile</div>
              </DropdownMenuItem>
              <DropdownMenuItem>
                <div className="flex">Settings</div>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                className="cursor-pointer"
                onClick={() => {
                  logout();
                  navigate("/auth/login");
                }}
              >
                <div className="flex flex-col text-red-500">Sign Out</div>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </div>
  );
};

export default Header;
