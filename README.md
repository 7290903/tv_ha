# Virtual TV for Home Assistant

Создаёт виртуальный `media_player` с типом телевизора. Команды включения и выключения вызывают две выбранные сущности `input_button`. Реальное состояние телевизора не отслеживается.

## Установка через HACS

1. Откройте HACS → Integrations → меню ⋮ → Custom repositories.
2. Добавьте `https://github.com/7290903/tv_ha`, категория **Integration**.
3. Установите **Virtual TV** и перезапустите Home Assistant.
4. Откройте Settings → Devices & services → Add integration → Virtual TV.
5. Выберите имя, кнопку POWER ON и кнопку POWER OFF.

## Настройка Яндекс Умного дома

Объедините настройки ниже с уже существующим разделом `yandex_smart_home:` в `configuration.yaml` (не создавайте второй одноимённый раздел):

```yaml
yandex_smart_home:
  entity_config:
    media_player.virtual_tv:
      name: Телевизор
      room: Гостиная
      type: devices.types.media_device.tv
      features:
        - turn_on_off
```

После изменения конфигурации перезагрузите интеграцию Yandex Smart Home и обновите список устройств в приложении «Дом с Алисой».

## Поведение

- Включение вызывает `input_button.press` для выбранной кнопки POWER ON.
- Выключение вызывает `input_button.press` для выбранной кнопки POWER OFF.
- Состояние физического телевизора не считывается. Сущность использует условное состояние IDLE и `assumed_state`, чтобы не выдавать нажатие кнопки за подтверждение включения.
- У интеграции только функции включения и выключения; громкость, каналы и воспроизведение не реализованы.
