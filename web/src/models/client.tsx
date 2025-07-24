export interface Client {
  id: string;
  user_id: string;
  profile_text: string;
  profile_location: string;
  expires_at: Date;
  created_at: Date;
}

export const initClient: Client = {
  id: "",
  user_id: "",
  profile_text: "",
  profile_location: "",
  expires_at: new Date(),
  created_at: new Date(),
};
