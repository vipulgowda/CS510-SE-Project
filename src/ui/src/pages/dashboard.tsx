import { useEffect, useState } from "react";
import { fetchAnalytics } from "@/lib/api";
import Navbar from "@/components/Navbar";
import { motion } from "framer-motion";
import "@/styles/globals.css";

export default function Dashboard() {
  const [analytics, setAnalytics] = useState<any>(null);

  useEffect(() => {
    fetchAnalytics().then((res) => setAnalytics(res.data));
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Navbar />
      <div className="container mx-auto px-4 pt-20">
        <h1 className="text-4xl font-bold mb-8 text-center bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          Expense Overview
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {analytics ? (
            <>
              <motion.div
                whileHover={{ scale: 1.03 }}
                transition={{ type: "spring", stiffness: 300 }}
                className="bg-white p-6 rounded-xl shadow-lg"
              >
                <h2 className="text-lg font-semibold text-gray-600 mb-2">Total Spent</h2>
                <p className="text-3xl font-bold text-blue-600">${analytics.total_spent}</p>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.03 }}
                transition={{ type: "spring", stiffness: 300 }}
                className="bg-white p-6 rounded-xl shadow-lg"
              >
                <h2 className="text-lg font-semibold text-gray-600 mb-2">Average Amount</h2>
                <p className="text-3xl font-bold text-purple-600">${analytics.average_amount.toFixed(2)}</p>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.03 }}
                transition={{ type: "spring", stiffness: 300 }}
                className="bg-white p-6 rounded-xl shadow-lg"
              >
                <h2 className="text-lg font-semibold text-gray-600 mb-2">Receipt Count</h2>
                <p className="text-3xl font-bold text-green-600">{analytics.receipt_count}</p>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.03 }}
                transition={{ type: "spring", stiffness: 300 }}
                className="bg-white p-6 rounded-xl shadow-lg"
              >
                <h2 className="text-lg font-semibold text-gray-600 mb-2">Top Vendor</h2>
                <p className="text-3xl font-bold text-orange-600">
                  {Object.entries(analytics.vendor_summary)
                    .sort(([,a]: any, [,b]: any) => b.total - a.total)[0][0]}
                </p>
              </motion.div>
            </>
          ) : (
            <div className="col-span-4 text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Loading your expense data...</p>
            </div>
          )}
        </div>

        {analytics && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white p-6 rounded-xl shadow-lg"
          >
            <h2 className="text-xl font-semibold mb-4">Vendor Breakdown</h2>
            <div className="space-y-4">
              {Object.entries(analytics.vendor_summary).map(([vendor, data]: [string, any]) => (
                <div key={vendor} className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-800">{vendor}</h3>
                    <p className="text-sm text-gray-500">{data.count} receipts</p>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold text-blue-600">${data.total}</p>
                    <p className="text-sm text-gray-500">
                      {((data.total / analytics.total_spent) * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
