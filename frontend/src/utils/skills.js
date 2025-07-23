export const processSkills = (raw) => {
    if (!raw) return []
    const clean = (arr) =>
      arr.filter(v => v != null && v !== '')
         .map(v => (typeof v === 'object' ? (v.value ?? v.label ?? '') : v) + '')
         .map(v => v.trim())
         .filter(v => v && v !== '[object Object]')
  
    if (Array.isArray(raw)) return clean(raw)
  
    if (typeof raw === 'string') {
      // ưu tiên parse JSON
      try {
        const parsed = JSON.parse(raw)
        if (Array.isArray(parsed)) return clean(parsed)
      } catch {/* ignore */}
      // fallback CSV
      return clean(raw.split(','))
    }
  
    if (typeof raw === 'object') return clean(Object.values(raw))
    return []
  }
  
  