import { NextApiRequest, NextApiResponse } from "next";
 import { getGoogleLoginUrl } from "../../lib/api";
 
 export default async function handler(req: NextApiRequest, res: NextApiResponse) {
   try {
     const authUrl = await getGoogleLoginUrl();
     res.redirect(authUrl);
   } catch (error) {
     res.status(500).json({ error: "Failed to fetch Google OAuth URL" });
   }
 }