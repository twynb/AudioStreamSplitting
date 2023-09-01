import { type Config } from 'driver.js'
import { driver as createDriver } from 'driver.js'

const driver = shallowRef(createDriver())

export function useDriver() {
  const { t } = useI18n()

  const forcedConfig: Config = {
    showButtons: ['next', 'previous'],
    smoothScroll: true,
    stagePadding: 10,
    stageRadius: 14,
    nextBtnText: t('button.next'),
    prevBtnText: t('button.previous'),
    doneBtnText: t('button.done'),
    showProgress: true,
  }

  function setConfig(config: Omit<Config, 'stagePadding' | 'stageRadius'>) {
    driver.value.setConfig({
      ...config,
      ...forcedConfig,
    })
  }

  return {
    driver,
    setConfig,
  }
}
