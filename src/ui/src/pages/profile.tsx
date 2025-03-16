import { useState, useEffect } from "react";
import Navbar from "@/components/Navbar";
import { motion } from "framer-motion";
import { useRouter } from "next/router";

export default function Profile() {
  const [authData, setAuthData] = useState<any>(null);
  const router = useRouter();

  useEffect(() => {
    // Check localStorage for auth data
    const stored = localStorage.getItem('authData');
    if (stored) {
      try {
        const parsedData = JSON.parse(stored);
        setAuthData(parsedData);
      } catch (error) {
        localStorage.removeItem('authData');
        router.push('/login');
      }
    } else {
      router.push('/login');
    }
  }, [router]);

  if (!authData) {
    return null; // or a loading spinner
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Navbar />
      <div className="container mx-auto px-4 pt-32 pb-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-3xl mx-auto"
        >
          <div className="bg-white p-8 rounded-2xl shadow-lg">
            <div className="flex items-center gap-6 mb-8">
              <img 
                src={authData.user.picture || ''} 
                className="w-40 h-40 rounded-full shadow-md object-cover bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white"
                onError={(e) => {
                  const target = e.target as HTMLImageElement;
                  const div = document.createElement('div');
                  div.className = "w-40 h-40 rounded-full shadow-md bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white text-6xl font-bold";
                  div.textContent = authData.user.name.charAt(0).toUpperCase();
                  target.parentNode?.replaceChild(div, target);
                }}
              />
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Profile
              </h1>
            </div>
            
            <div className="space-y-6">
              <div className="border-b pb-4">
                <h2 className="text-lg font-semibold text-gray-600 mb-2">User Information</h2>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-500">Full Name</p>
                    <p className="text-lg">{authData.user.name}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Email</p>
                    <p className="text-lg">{authData.user.email}</p>
                  </div>
                </div>
              </div>

              <div className="border-b pb-4">
                <h2 className="text-lg font-semibold text-gray-600 mb-2">Additional Details</h2>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-500">Given Name</p>
                    <p className="text-lg">{authData.user.given_name}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Family Name</p>
                    <p className="text-lg">{authData.user.family_name}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Organization</p>
                    <p className="text-lg">{authData.user.hd}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Email Status</p>
                    <p className="text-lg flex items-center gap-2">
                      {authData.user.verified_email ? (
                        <>
                          <span className="text-green-600">✓</span> Verified
                        </>
                      ) : (
                        <>
                          <span className="text-red-600">✗</span> Unverified
                        </>
                      )}
                    </p>
                  </div>
                </div>
              </div>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg shadow-md hover:shadow-lg transition-all duration-200"
                onClick={() => {
                  localStorage.removeItem('authData');
                  router.push('/login');
                }}
              >
                Sign Out
              </motion.button>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
} 