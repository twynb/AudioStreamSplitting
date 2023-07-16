import { mount } from '@vue/test-utils'
import BaseBadge from './BaseBadge.vue'

test('mount component', async () => {
  const component = mount(BaseBadge, { props: { content: 'foo' } })
  expect(component.html()).toContain('foo')
})
