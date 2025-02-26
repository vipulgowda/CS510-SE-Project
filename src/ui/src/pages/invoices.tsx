import { useEffect, useState } from "react";
import { fetchReceipts, deleteReceipt, updateReceipt } from "@/lib/api";
import Navbar from "@/components/Navbar";
import { motion } from "framer-motion";
import "@/styles/globals.css";

export default function Receipts() {
  const [receipts, setReceipts] = useState<any>([]);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editForm, setEditForm] = useState<any>({});

  useEffect(() => {
    fetchReceipts().then((res) => setReceipts(res.data));
  }, []);

  const handleDelete = async (id: number) => {
    try {
      await deleteReceipt(id);
      setReceipts(receipts.filter((r: any) => r.id !== id));
    } catch (error) {
      console.error('Failed to delete receipt:', error);
    }
  };

  const handleEdit = (receipt: any) => {
    setEditingId(receipt.id);
    setEditForm(receipt);
  };

  const handleSave = async () => {
    try {
      await updateReceipt(editingId!, editForm);
      setReceipts(receipts.map((r: any) => 
        r.id === editingId ? editForm : r
      ));
      setEditingId(null);
    } catch (error) {
      console.error('Failed to update receipt:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Navbar />
      <div className="container mx-auto px-4 pt-20">
        <h1 className="text-4xl font-bold mb-8 text-center bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          Receipts
        </h1>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white p-6 rounded-xl shadow-lg"
        >
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="px-6 py-3 text-left text-gray-600">Vendor</th>
                  <th className="px-6 py-3 text-left text-gray-600">Amount</th>
                  <th className="px-6 py-3 text-left text-gray-600">Date</th>
                  <th className="px-6 py-3 text-left text-gray-600">Bill Type</th>
                  <th className="px-6 py-3 text-left text-gray-600">City</th>
                  <th className="px-6 py-3 text-left text-gray-600">State</th>
                  <th className="px-6 py-3 text-left text-gray-600">Country</th>
                  <th className="px-6 py-3 text-right text-gray-600">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {receipts.map((receipt: any) => (
                  <motion.tr
                    key={receipt.id}
                    whileHover={{ backgroundColor: "rgba(59, 130, 246, 0.05)" }}
                    className="group"
                  >
                    {editingId === receipt.id ? (
                      <>
                        <td className="px-6 py-4">
                          <input
                            className="w-full p-2 border rounded"
                            value={editForm.vendor_name}
                            onChange={(e) => setEditForm({...editForm, vendor_name: e.target.value})}
                          />
                        </td>
                        <td className="px-6 py-4">
                          <input
                            className="w-full p-2 border rounded"
                            type="number"
                            value={editForm.total_amount}
                            onChange={(e) => setEditForm({...editForm, total_amount: e.target.value})}
                          />
                        </td>
                        <td className="px-6 py-4">
                          <input
                            className="w-full p-2 border rounded"
                            type="date"
                            value={editForm.date_time?.split('T')[0]}
                            onChange={(e) => setEditForm({...editForm, date_time: e.target.value})}
                          />
                        </td>
                        <td className="px-6 py-4">
                          <input
                            className="w-full p-2 border rounded"
                            value={editForm.bill_type}
                            onChange={(e) => setEditForm({...editForm, bill_type: e.target.value})}
                          />
                        </td>
                        <td className="px-6 py-4">
                          <input
                            className="w-full p-2 border rounded"
                            value={editForm.city === 'nan' ? '' : editForm.city}
                            onChange={(e) => setEditForm({...editForm, city: e.target.value})}
                          />
                        </td>
                        <td className="px-6 py-4">
                          <input
                            className="w-full p-2 border rounded"
                            value={editForm.state === 'nan' ? '' : editForm.state}
                            onChange={(e) => setEditForm({...editForm, state: e.target.value})}
                          />
                        </td>
                        <td className="px-6 py-4">
                          <input
                            className="w-full p-2 border rounded"
                            value={editForm.country === 'nan' ? '' : editForm.country}
                            onChange={(e) => setEditForm({...editForm, country: e.target.value})}
                          />
                        </td>
                        <td className="px-6 py-4 text-right space-x-2">
                          <button
                            onClick={handleSave}
                            className="text-green-600 hover:text-green-800"
                          >
                            Save
                          </button>
                          <button
                            onClick={() => setEditingId(null)}
                            className="text-gray-600 hover:text-gray-800"
                          >
                            Cancel
                          </button>
                        </td>
                      </>
                    ) : (
                      <>
                        <td className="px-6 py-4 text-gray-800">{receipt.vendor_name}</td>
                        <td className="px-6 py-4 text-gray-800">${receipt.total_amount}</td>
                        <td className="px-6 py-4 text-gray-800">{receipt.date_time?.split('T')[0]}</td>
                        <td className="px-6 py-4 text-gray-800">{receipt.bill_type}</td>
                        <td className="px-6 py-4 text-gray-800">{receipt.city === 'nan' ? '' : receipt.city}</td>
                        <td className="px-6 py-4 text-gray-800">{receipt.state === 'nan' ? '' : receipt.state}</td>
                        <td className="px-6 py-4 text-gray-800">{receipt.country === 'nan' ? '' : receipt.country}</td>
                        <td className="px-6 py-4 text-right space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button
                            onClick={() => handleEdit(receipt)}
                            className="text-blue-600 hover:text-blue-800"
                          >
                            Edit
                          </button>
                          <button
                            onClick={() => handleDelete(receipt.id)}
                            className="text-red-600 hover:text-red-800"
                          >
                            Delete
                          </button>
                        </td>
                      </>
                    )}
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
