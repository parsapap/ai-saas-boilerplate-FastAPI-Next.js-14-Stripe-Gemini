"use client";

import { useState, useEffect } from "react";
import { createPortal } from "react-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, Building2, Check, X, Loader2 } from "lucide-react";
import { organizationApi } from "@/lib/api";
import { toast } from "sonner";

interface Organization {
  id: number;
  name: string;
  slug: string;
  user_role: string;
}

export function OrganizationSwitcher() {
  const [isOpen, setIsOpen] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [selected, setSelected] = useState<Organization | null>(null);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  
  const [formData, setFormData] = useState({
    name: "",
    slug: "",
    description: "",
  });
  const [slugManuallyEdited, setSlugManuallyEdited] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    loadOrganizations();
  }, []);

  const loadOrganizations = async () => {
    try {
      setLoading(true);
      const orgs = await organizationApi.list();
      setOrganizations(orgs);
      
      // Set first org as selected or get from localStorage
      const savedOrgId = localStorage.getItem('current_org_id');
      if (savedOrgId) {
        const savedOrg = orgs.find((o: Organization) => o.id === parseInt(savedOrgId));
        if (savedOrg) {
          setSelected(savedOrg);
        } else if (orgs.length > 0) {
          setSelected(orgs[0]);
          localStorage.setItem('current_org_id', orgs[0].id.toString());
        }
      } else if (orgs.length > 0) {
        setSelected(orgs[0]);
        localStorage.setItem('current_org_id', orgs[0].id.toString());
      }
    } catch (error: any) {
      console.error('Failed to load organizations:', error);
      toast.error('Failed to load organizations');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectOrg = (org: Organization) => {
    setSelected(org);
    localStorage.setItem('current_org_id', org.id.toString());
    setIsOpen(false);
    // Reload page to update context
    window.location.reload();
  };

  const handleCreateOrg = async (e: React.FormEvent) => {
    e.preventDefault();
    
    console.log('Form submitted with data:', formData);
    
    if (!formData.name.trim() || !formData.slug.trim()) {
      toast.error('Name and slug are required');
      return;
    }

    // Validate slug format
    if (!/^[a-z0-9-]+$/.test(formData.slug)) {
      toast.error('Slug must contain only lowercase letters, numbers, and hyphens');
      return;
    }

    try {
      setCreating(true);
      console.log('Creating organization...');
      const newOrg = await organizationApi.create(
        formData.name,
        formData.slug,
        formData.description || undefined
      );
      
      console.log('Organization created:', newOrg);
      toast.success('Organization created successfully!');
      
      // Add to list and select it
      const orgWithRole = { ...newOrg, user_role: 'owner' };
      setOrganizations([...organizations, orgWithRole]);
      setSelected(orgWithRole);
      localStorage.setItem('current_org_id', newOrg.id.toString());
      
      // Reset form and close modal
      setFormData({ name: "", slug: "", description: "" });
      setSlugManuallyEdited(false);
      setShowCreateModal(false);
      setIsOpen(false);
      
      // Reload to update context
      window.location.reload();
    } catch (error: any) {
      console.error('Failed to create organization:', error);
      const message = error.response?.data?.detail || 'Failed to create organization';
      toast.error(message);
    } finally {
      setCreating(false);
    }
  };

  const generateSlug = (name: string) => {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .trim();
  };

  if (loading) {
    return (
      <div className="flex items-center gap-2 px-4 py-2 rounded-lg border border-white/10 bg-white/5">
        <Loader2 className="w-4 h-4 animate-spin" />
        <span className="text-sm">Loading...</span>
      </div>
    );
  }

  return (
    <>
      <div className="relative">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-2 px-4 py-2 rounded-lg border border-white/10 bg-white/5 hover:bg-white/10 transition-all duration-300"
        >
          <Building2 className="w-4 h-4" />
          <span className="text-sm font-medium">{selected?.name || 'Select Organization'}</span>
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
                  {organizations.length === 0 ? (
                    <div className="px-3 py-4 text-center text-sm text-white/40">
                      No organizations yet
                    </div>
                  ) : (
                    organizations.map((org, index) => (
                      <motion.button
                        key={org.id}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.05 }}
                        onClick={() => handleSelectOrg(org)}
                        className="w-full flex items-center justify-between px-3 py-2 rounded-md hover:bg-white/10 transition-colors duration-200"
                      >
                        <div className="flex items-center gap-3">
                          <Building2 className="w-4 h-4 text-white/60" />
                          <div className="text-left">
                            <div className="text-sm font-medium">{org.name}</div>
                            <div className="text-xs text-white/40">{org.slug}</div>
                          </div>
                        </div>
                        {selected?.id === org.id && (
                          <motion.div
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            transition={{ type: "spring", stiffness: 500, damping: 30 }}
                          >
                            <Check className="w-4 h-4 text-white" />
                          </motion.div>
                        )}
                      </motion.button>
                    ))
                  )}
                </div>
                <div className="border-t border-white/10 p-2">
                  <button 
                    onClick={() => {
                      setShowCreateModal(true);
                      setIsOpen(false);
                    }}
                    className="w-full px-3 py-2 text-sm text-white/60 hover:text-white hover:bg-white/5 rounded-md transition-all duration-200"
                  >
                    + Create Organization
                  </button>
                </div>
              </motion.div>
            </>
          )}
        </AnimatePresence>
      </div>

      {/* Create Organization Modal - Rendered via Portal */}
      {mounted && showCreateModal && createPortal(
        <AnimatePresence>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-[9999] flex items-center justify-center p-4"
            style={{ margin: 0 }}
            onClick={(e) => {
              if (e.target === e.currentTarget && !creating) {
                setShowCreateModal(false);
              }
            }}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              transition={{ duration: 0.2 }}
              className="bg-black border border-white/10 rounded-xl p-6 w-full max-w-md relative"
            >
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold">Create Organization</h2>
                  <button
                    onClick={() => !creating && setShowCreateModal(false)}
                    disabled={creating}
                    className="text-white/40 hover:text-white transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                <form onSubmit={handleCreateOrg} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Organization Name *
                    </label>
                    <input
                      type="text"
                      value={formData.name}
                      onChange={(e) => {
                        const name = e.target.value;
                        setFormData({
                          ...formData,
                          name,
                          slug: slugManuallyEdited ? formData.slug : generateSlug(name),
                        });
                      }}
                      placeholder="Acme Corp"
                      disabled={creating}
                      className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20 disabled:opacity-50"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Slug * <span className="text-white/40 text-xs">(lowercase, numbers, hyphens)</span>
                    </label>
                    <input
                      type="text"
                      value={formData.slug}
                      onChange={(e) => {
                        setSlugManuallyEdited(true);
                        setFormData({ ...formData, slug: e.target.value.toLowerCase() });
                      }}
                      placeholder="acme-corp"
                      disabled={creating}
                      className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20 disabled:opacity-50"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Description
                    </label>
                    <textarea
                      value={formData.description}
                      onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                      placeholder="Optional description..."
                      rows={3}
                      disabled={creating}
                      className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20 resize-none disabled:opacity-50"
                    />
                  </div>

                  <div className="flex gap-3 pt-4">
                    <button
                      type="button"
                      onClick={() => setShowCreateModal(false)}
                      disabled={creating}
                      className="flex-1 px-4 py-2 border border-white/10 rounded-lg hover:bg-white/5 transition-colors disabled:opacity-50"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      disabled={creating || !formData.name.trim() || !formData.slug.trim()}
                      onClick={(e) => {
                        console.log('Button clicked!', {
                          creating,
                          name: formData.name,
                          slug: formData.slug,
                          disabled: creating || !formData.name.trim() || !formData.slug.trim()
                        });
                      }}
                      className="flex-1 px-4 py-2 bg-white text-black rounded-lg hover:bg-white/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                      {creating ? (
                        <>
                          <Loader2 className="w-4 h-4 animate-spin" />
                          Creating...
                        </>
                      ) : (
                        'Create'
                      )}
                    </button>
                  </div>
                </form>
              </motion.div>
            </motion.div>
        </AnimatePresence>,
        document.body
      )}
    </>
  );
}
