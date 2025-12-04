"use client";

import { motion } from "framer-motion";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const data = [
  { day: "Mon", messages: 12 },
  { day: "Tue", messages: 19 },
  { day: "Wed", messages: 15 },
  { day: "Thu", messages: 25 },
  { day: "Fri", messages: 22 },
  { day: "Sat", messages: 18 },
  { day: "Sun", messages: 14 },
];

export function ActivityChart() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3, duration: 0.5 }}
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
      className="p-6 rounded-xl bg-white/5 backdrop-blur-xl border border-white/10 hover:border-white/20 transition-all duration-300"
    >
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-1">Activity</h3>
        <p className="text-sm text-white/60">Last 7 days usage (sample data)</p>
      </div>

      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
          <XAxis
            dataKey="day"
            stroke="#ffffff40"
            style={{ fontSize: "12px" }}
          />
          <YAxis stroke="#ffffff40" style={{ fontSize: "12px" }} />
          <Tooltip
            contentStyle={{
              backgroundColor: "#000000dd",
              border: "1px solid #ffffff20",
              borderRadius: "8px",
              backdropFilter: "blur(20px)",
            }}
            labelStyle={{ color: "#ffffff" }}
          />
          <Line
            type="monotone"
            dataKey="messages"
            stroke="#ffffff"
            strokeWidth={2}
            dot={{ fill: "#ffffff", r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </motion.div>
  );
}
