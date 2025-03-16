import { useEffect, useState } from "react";
import { getGoogleLoginUrl, getUserSession, logoutUser } from "../lib/api";
import { motion } from "framer-motion";

export default function Login() {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    getUserSession()
      .then((res: { data: { user: any; }; }) => setUser(res.data.user))
      .catch(() => setUser(null));
  }, []);

  const handleLogin = async () => {
    const authUrl = await getGoogleLoginUrl();
    window.location.href = authUrl;
  };

  const handleLogout = async () => {
    await logoutUser();
    setUser(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 pt-32 pb-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-md mx-auto text-center"
        >
          <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Welcome
          </h1>
          <p className="text-xl text-gray-600 mb-12">
            Sign in to manage your receipts and expenses
          </p>

          <motion.div
            className="bg-white p-8 rounded-2xl shadow-lg"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            {!user ? (
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleLogin}
                className="w-full px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-200"
              >
                Sign in with Google
              </motion.button>
            ) : (
              <div className="space-y-4">
                <p className="text-xl font-semibold text-gray-800">Welcome, {user.name}</p>
                <p className="text-gray-600">{user.email}</p>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleLogout}
                  className="px-8 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-all duration-200"
                >
                  Logout
                </motion.button>
              </div>
            )}
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}
