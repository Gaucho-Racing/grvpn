import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { checkCredentials } from "@/lib/auth";
import Footer from "@/components/Footer";
import { AuthLoading } from "@/components/AuthLoading";
import { useUser } from "@/lib/store";
import Header from "@/components/Header";
import { Client, initClient } from "@/models/client";
import { BACKEND_URL } from "@/consts/config";
import axios from "axios";
import { notify } from "@/lib/notify";
import { getAxiosErrorMessage } from "@/lib/axios-error-handler";
import { OutlineButton } from "@/components/ui/outline-button";
import { Plus } from "lucide-react";
import { NoProfilesCard } from "@/components/NoProfilesCard";
import { NoExpiredProfilesCard } from "@/components/NoExpiredProfilesCard";
import { ProfileCard } from "@/components/ProfileCard";

function App() {
  const navigate = useNavigate();
  const currentUser = useUser();

  const [clients, setClients] = useState<Client[]>([]);
  const [expiredClients, setExpiredClients] = useState<Client[]>([]);

  React.useEffect(() => {
    checkAuth().then(() => {});
  }, []);

  React.useEffect(() => {
    if (currentUser.id != "") {
      getClients();
      getExpiredClients();
    }
  }, [currentUser.id]);

  const checkAuth = async () => {
    const currentRoute = window.location.pathname + window.location.search;
    const status = await checkCredentials();
    if (status != 0) {
      if (currentRoute == "/") {
        navigate(`/auth/login`);
      } else {
        navigate(`/auth/login?route=${encodeURIComponent(currentRoute)}`);
      }
    }
  };

  const getClients = async () => {
    try {
      const response = await axios.get(
        `${BACKEND_URL}/users/${currentUser.id}/clients`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("sentinel_access_token")}`,
          },
        },
      );
      setClients(response.data);
    } catch (error: any) {
      notify.error(getAxiosErrorMessage(error));
      console.error(error);
    }
  };

  const getExpiredClients = async () => {
    try {
      const response = await axios.get(
        `${BACKEND_URL}/users/${currentUser.id}/clients/expired`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("sentinel_access_token")}`,
          },
        },
      );
      setExpiredClients(response.data);
    } catch (error: any) {
      notify.error(getAxiosErrorMessage(error));
      console.error(error);
    }
  };

  const createClient = async () => {
    try {
      await axios.post(
        `${BACKEND_URL}/clients`,
        { ...initClient, user_id: currentUser.id },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("sentinel_access_token")}`,
          },
        },
      );
      notify.success("VPN Profile created successfully");
      getClients();
      getExpiredClients();
    } catch (error: any) {
      notify.error(getAxiosErrorMessage(error));
      console.error(error);
    }
  };

  return (
    <>
      {currentUser.id == "" ? (
        <AuthLoading />
      ) : (
        <div className="flex h-screen flex-col justify-between">
          <Header />
          <div className="flex flex-grow flex-col justify-start p-4 lg:p-32 lg:pt-16">
            <div className="flex flex-row items-center justify-between">
              <h2>Active Profiles</h2>
              <OutlineButton onClick={createClient}>
                <div className="flex items-center gap-2">
                  <Plus className="h-5 w-5" />
                  Create Profile
                </div>
              </OutlineButton>
            </div>
            <div className="mt-4 flex flex-col gap-2">
              {clients.length === 0 ? (
                <NoProfilesCard />
              ) : (
                clients.map((client) => (
                  <ProfileCard key={client.id} client={client} />
                ))
              )}
            </div>
            <div className="flex flex-row items-center justify-between pt-8">
              <h2>Expired Profiles</h2>
            </div>
            <div className="mt-4 flex flex-col gap-2">
              {expiredClients.length === 0 ? (
                <NoExpiredProfilesCard />
              ) : (
                expiredClients.map((client) => (
                  <ProfileCard key={client.id} client={client} />
                ))
              )}
            </div>
          </div>
          <Footer />
        </div>
      )}
    </>
  );
}

export default App;
