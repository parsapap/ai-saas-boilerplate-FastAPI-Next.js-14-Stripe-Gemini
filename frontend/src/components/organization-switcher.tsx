"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, Building2, Check } from "lucide-react";

interface Organization {
  id: string;
  name: string;
  slug: string;
}

const mockOrgs: Organization[] = [
  { id: "1", name: "Personal Workspace", slug: "personal" },
  { id: "2", name: "Acme Corp", slug: "acme" },
  { id: "3", name: "Startup Inc", slug: "startup" },
];

export function OrganizationSwitcher() {
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState(mockOrgs[0]);

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 rounded-lg border border-white/10 bg-white/5 hover:bg-white/10 transition-all duration-300"
      >
        <Building2 className="w-4 h-4" />
        <span className="text-sm font-medium">{selected.name}</span>
        <motion.div
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.3 }}
        >
          <ChevronDown className="w-4 h-4" />
        </motion.div>
      </button>

      <AnimatePresence>
        {isOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-40"
              onClick={() => setIsOpen(false)}
            />
            <motion.div
              initial={{ opacity: 0, y: -10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -10, scale: 0.95 }}
              transition={{ duration: 0.2 }}
              className="absolute top-full mt-2 right-0 w-64 bg-black/90 backdrop-blur-xl border border-white/10 rounded-lg shadow-2xl z-50 overflow-hidden"
            >
              <div className="p-2">
                {mockOrgs.map((org, index) => (
                  <motion.button
                    key={org.id}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    onClick={() => {
                      setSelected(org);
                      setIsOpen(false);
                    }}
                    className="w-full flex items-center justify-between px-3 py-2 rounded-md hover:bg-white/10 transition-colors duration-200"
                  >
                    <div className="flex items-center gap-3">
                      <Building2 className="w-4 h-4 text-white/60" />
                      <div className="text-left">
                        <div className="text-sm font-medium">{org.name}</div>
                        <div className="text-xs text-white/40">{org.slug}</div>
                      </div>
                    </div>
                    {selected.id === org.id && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ type: "spring", stiffness: 500, damping: 30 }}
                      >
                        <Check className="w-4 h-4 text-white" />
                      </motion.div>
                    )}
                  </motion.button>
                ))}
              </div>
              <div className="border-t border-white/10 p-2">
                <button className="w-full px-3 py-2 text-sm text-white/60 hover:text-white hover:bg-white/5 rounded-md transition-all duration-200">
                  + Create Organization
                </button>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
}
