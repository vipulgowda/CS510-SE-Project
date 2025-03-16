import { NextApiRequest, NextApiResponse } from "next";
 import axios from "axios";
 
 export default async function handler(req: NextApiRequest, res: NextApiResponse) {
   if (req.method !== "GET") {
     return res.status(405).json({ error: "Method Not Allowed" });
   }
 
   const { code } = req.query;
 
   if (!code) {
     return res.status(400).json({ error: "Authorization code missing" });
   }
 
   try {
     // Ensure the request is a GET request
     const response = await axios.get(`http://localhost:5000/api/v1/auth/callback?code=${code}`);
     // Redirect to homepage with auth data as URL parameters
     const authData = encodeURIComponent(JSON.stringify(response.data));
     res.redirect(`/?auth=${authData}`);
   } catch (error) {
     res.status(500).json({ error: "Failed to authenticate" });
   }
 }
 