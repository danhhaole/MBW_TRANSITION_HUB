import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { call } from 'frappe-ui'

export const useCampaignQRStore = defineStore('campaignQR', () => {
  // State
  const qrCodes = ref([])
  const currentQR = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const getQRCodesByCampaign = computed(() => (campaignId) => {
    return qrCodes.value.filter(qr => qr.campaign_id === campaignId)
  })

  // Actions
  const fetchQRCodesByCampaign = async (campaignId) => {
    loading.value = true
    error.value = null

    try {
      const result = await call('frappe.client.get_list', {
        doctype: 'Mira Campaign QR',
        filters: { campaign_id: campaignId },
        fields: [
          'name',
          'campaign_id',
          'qr_name',
          'description',
          'purpose',
          'landing_page_url',
          'utm_campaign',
          'utm_source',
          'utm_medium',
          'qr_url',
          'qr_image',
          'qr_data',
          'creation',
          'modified'
        ],
        order_by: 'creation desc'
      })

      if (result) {
        qrCodes.value = result
        return { success: true, data: result }
      }

      return { success: false, error: 'No data returned' }
    } catch (err) {
      error.value = parseError(err)
      console.error('Error fetching QR codes:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const fetchQRCodeById = async (qrId) => {
    loading.value = true
    error.value = null

    try {
      const result = await call('frappe.client.get', {
        doctype: 'Mira Campaign QR',
        name: qrId
      })

      if (result) {
        currentQR.value = result
        return { success: true, data: result }
      }

      return { success: false, error: 'No data returned' }
    } catch (err) {
      error.value = parseError(err)
      console.error('Error fetching QR code:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const createQRCode = async (qrData) => {
    loading.value = true
    error.value = null

    try {
      // Validate required fields
      if (!qrData.campaign_id) {
        throw new Error('Campaign ID is required')
      }
      if (!qrData.qr_name) {
        throw new Error('QR Name is required')
      }

      const result = await call('frappe.client.insert', {
        doc: {
          doctype: 'Mira Campaign QR',
          campaign_id: qrData.campaign_id,
          qr_name: qrData.qr_name,
          description: qrData.description || '',
          purpose: qrData.purpose || '',
          landing_page_url: qrData.landing_page_url || '',
          utm_campaign: qrData.utm_campaign || qrData.campaign_id,
          utm_source: qrData.utm_source || 'qr_code',
          utm_medium: qrData.utm_medium || 'qr',
          qr_url: qrData.qr_url || '',
          qr_image: qrData.qr_image || '',
          qr_data: qrData.qr_data || null
        }
      })

      if (result && result.name) {
        // Add to local state
        qrCodes.value.unshift(result)
        return { success: true, data: result }
      }

      return { success: false, error: 'Failed to create QR code' }
    } catch (err) {
      error.value = parseError(err)
      console.error('Error creating QR code:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const updateQRCode = async (qrId, qrData) => {
    loading.value = true
    error.value = null

    try {
      const result = await call('frappe.client.set_value', {
        doctype: 'Mira Campaign QR',
        name: qrId,
        fieldname: qrData
      })

      if (result) {
        // Update in local state
        const index = qrCodes.value.findIndex(qr => qr.name === qrId)
        if (index !== -1) {
          qrCodes.value[index] = { ...qrCodes.value[index], ...qrData }
        }

        if (currentQR.value && currentQR.value.name === qrId) {
          currentQR.value = { ...currentQR.value, ...qrData }
        }

        return { success: true, data: result }
      }

      return { success: false, error: 'Failed to update QR code' }
    } catch (err) {
      error.value = parseError(err)
      console.error('Error updating QR code:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const deleteQRCode = async (qrId) => {
    loading.value = true
    error.value = null

    try {
      await call('frappe.client.delete', {
        doctype: 'Mira Campaign QR',
        name: qrId
      })

      // Remove from local state
      qrCodes.value = qrCodes.value.filter(qr => qr.name !== qrId)

      if (currentQR.value && currentQR.value.name === qrId) {
        currentQR.value = null
      }

      return { success: true }
    } catch (err) {
      error.value = parseError(err)
      console.error('Error deleting QR code:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const generateQRCode = async (qrId, landingPageUrl, utmParams) => {
    loading.value = true
    error.value = null

    try {
      const result = await call('mbw_mira.api.create_landing_page_qrcode', {
        landing_page_url: landingPageUrl,
        campaign_id: utmParams.utm_campaign,
        utm_source: utmParams.utm_source,
        utm_medium: utmParams.utm_medium,
        utm_campaign: utmParams.utm_campaign
      })

      if (result?.status === 'success' && result?.data) {
        // Update QR code with generated data
        await updateQRCode(qrId, {
          qr_image: result.data.qr_image,
          qr_url: result.data.url,
          qr_data: result.data
        })

        return { success: true, data: result.data }
      }

      return { success: false, error: 'Failed to generate QR code' }
    } catch (err) {
      error.value = parseError(err)
      console.error('Error generating QR code:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Helper functions
  const parseError = (error) => {
    if (typeof error === 'string') return error
    if (error.message) return error.message
    if (error.exc) {
      try {
        const exc = JSON.parse(error.exc)
        if (exc && exc.message) return exc.message
      } catch (e) {
        return error.exc
      }
    }
    return 'An unexpected error occurred'
  }

  const clearError = () => {
    error.value = null
  }

  const clearCurrentQR = () => {
    currentQR.value = null
  }

  return {
    // State
    qrCodes,
    currentQR,
    loading,
    error,

    // Getters
    getQRCodesByCampaign,

    // Actions
    fetchQRCodesByCampaign,
    fetchQRCodeById,
    createQRCode,
    updateQRCode,
    deleteQRCode,
    generateQRCode,
    clearError,
    clearCurrentQR
  }
})
