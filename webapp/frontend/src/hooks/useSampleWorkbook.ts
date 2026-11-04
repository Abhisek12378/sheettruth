// Loads the bundled sample workbook so a visitor without a spreadsheet can try an audit.
// The sample is served with the front end's static files and handed to the uploader as an
// ordinary File, so it goes through the same upload path as a dropped workbook.

import { useCallback, useState } from 'react'

export const SAMPLE_WORKBOOK = {
  name: 'southpoint-gas-model.xlsx',
  path: '/samples/southpoint-gas-model.xlsx',
  description: 'A real gas usage model with two formula errors.',
}

const WORKBOOK_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
const LOAD_ERROR = 'The sample workbook could not be loaded. Please try again, or upload a workbook of your own.'

async function fetchSample(): Promise<File> {
  const response = await fetch(SAMPLE_WORKBOOK.path)
  if (!response.ok) throw new Error(LOAD_ERROR)
  const blob = await response.blob()
  return new File([blob], SAMPLE_WORKBOOK.name, { type: WORKBOOK_TYPE })
}

export function useSampleWorkbook(onLoaded: (file: File) => void, onError: (message: string) => void) {
  const [loading, setLoading] = useState(false)

  const load = useCallback(() => {
    setLoading(true)
    fetchSample()
      .then(onLoaded)
      .catch(() => onError(LOAD_ERROR))
      .finally(() => setLoading(false))
  }, [onLoaded, onError])

  return { loading, load }
}
