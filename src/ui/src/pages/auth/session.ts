import { NextApiRequest, NextApiResponse } from "next";
 import { getUserSession } from "../../lib/api";
 
 export default async function handler(req: NextApiRequest, res: NextApiResponse) {
   try {
     const response = await getUserSession();
     res.status(200).json(response.data);
   } catch (error) {
     res.status(401).json({ error: "User not authenticated" });
   }
 }
 