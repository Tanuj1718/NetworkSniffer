"use client";

import { useEffect, useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { io, Socket } from "socket.io-client";

export default function Dashboard() {
  const [logs, setLogs] = useState<string[]>([]);
  const [filters, setFilters] = useState<string>("");
  const [devices, setDevices] = useState<{ name: string, ip: string }[]>([]); // To store device details
  const socketRef = useRef<Socket | null>(null);

  // Convert filter text to array
  const filterList = filters
    .split("\n")
    .map((d) => d.trim().toLowerCase())
    .filter(Boolean);

  useEffect(() => {
    // Socket connection
    const socket = io("http://localhost:5050", {
      transports: ["websocket", "polling"],
    });

    socketRef.current = socket;

    // Connection established
    socket.on("connect", () => {
      console.log("[SocketIO] Connected");
    });

    // Handle new domain logs
    socket.on("new_log", (data) => {
        setLogs(prevLogs => [
            `${data.device_ip} (${data.device_name}) → ${data.domain}`, ...prevLogs
          ])
    });

    // Handle new device logs
    socket.on("new_device_log", (data) => {
      setDevices((prevDevices) => [...prevDevices, { name: data.device_name, ip: data.device_ip }]);
    });

    // Load existing filters from backend
    fetch("http://localhost:5050/api/filters")
      .then((res) => res.json())
      .then((data) => setFilters(data.domains.join("\n")));

    // Disconnect on cleanup
    return () => {
      socket.disconnect();
    };
  }, []);

  // Update filter list on backend
  const updateFilters = () => {
    const updatedDomains = filters
      .split("\n")
      .map((domain) => domain.trim())
      .filter(Boolean);

    fetch("http://localhost:5050/api/filters", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ domains: updatedDomains }),
    }).then(() => alert("Filters updated!"));
  };

  return (
    <main className="p-4 max-w-3xl mx-auto text-black">
      <h1 className="text-2xl font-bold mb-4">🔍 Real-Time Domain Monitor</h1>

      {/* Live Logs */}
      <section className="mb-8">
        <h2 className="text-lg font-semibold mb-2">Live Logs</h2>
        <ul className="bg-gray-100 rounded p-4 h-64 overflow-auto border space-y-1">
          {logs.map((log, idx) => {
            const isFiltered = filterList.includes(log.toLowerCase());
            return (
              <li
                key={idx}
                className={`text-sm ${
                  isFiltered ? "text-red-600 font-semibold" : "text-blue-800"
                }`}
              >
                {isFiltered ? "🚫 " : "🌐 "}
                {log}
              </li>
            );
          })}
        </ul>
      </section>

      {/* Edit Filters */}
      <section>
        <h2 className="text-lg font-semibold mb-2">Edit Filtered Domains</h2>
        <Textarea
          value={filters}
          onChange={(e) => setFilters(e.target.value)}
          rows={6}
          className="w-full mb-2"
        />
        <Button onClick={updateFilters}>Update Filters</Button>
      </section>

      {/* Device Logs */}
      <section className="mt-8">
        <h2 className="text-lg font-semibold mb-2">Detected Devices</h2>
        <ul className="bg-gray-100 rounded p-4 h-64 overflow-auto border space-y-1">
          {devices.map((device, idx) => (
            <li key={idx} className="text-sm text-green-800">
              🚗 {device.name ? device.name : "Unnamed Device"} - {device.ip}
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}