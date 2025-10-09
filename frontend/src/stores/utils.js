import { defineStore } from "pinia"
import { getCachedResource, createResource, createListResource } from "frappe-ui"


export const useResourceStore = defineStore("resourceStore", {
 state: () => ({
   resources: {} // key: resourceName, value: resource
 }),
 actions: {
   getOrCreateResource({ key, doctype, name, auto = true }) {
     // 1. Kiểm tra cache global
     let resource = getCachedResource(`${doctype}/${name}`)
     if (resource) {
       return resource
     }


     // 2. Nếu chưa có thì tạo mới
     resource = createResource({
       url: "frappe.client.get",
       params: { doctype, name },
       auto
     })


     // 3. Lưu vào local store
     this.resources[key || `${doctype}/${name}`] = resource


     return resource
   }
 }
})


export const useListResourceStore = defineStore("listResourceStore", {
    state: () => ({
      listResources: {} // key -> list resource
    }),
    actions: {
      getOrCreateListResource({ key, doctype, fields, filters = {}, orderBy, auto = true, pageLength = 20 }) {
        // 1. Check global cache
        let resource = getCachedResource(key)
        if (resource) {
          return resource
        }
   
   
        // 2. Nếu chưa có thì tạo list resource
        resource = createListResource({
          doctype,
          fields,
          filters,
          order_by: orderBy,
          pageLength,
          auto
        })
   
   
        // 3. Lưu vào store
        this.listResources[key] = resource
   
   
        return resource
      }
    }
   })
   