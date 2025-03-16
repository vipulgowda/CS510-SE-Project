import { NextApiRequest, NextApiResponse } from "next";
 import { logoutUser } from "../../lib/api";
 
 export default async function handler(req: NextApiRequest, res: NextApiResponse) {
   try {
     await logoutUser();
     res.status(200).json({ message: "Logout successful" });
   } catch (error) {
     res.status(500).json({ error: "Logout failed" });
   }
 }
 