from ajenti.api import *


class UIProperty (object):
	def __init__(self, name, value):
		self.dirty = False
		self.name = name
		self.value = value

	def get(self):
		return self.value

	def set(self, value):
		self.value = value
		self.dirty = True


@interface
class UIElement (object):
	id = None

	def __init__(self, id=None, **kwargs):
		if id is not None:
			self.id = id
		if not hasattr(self, '_properties'):
			self._properties = []
		self.children = []
		self.properties = {}
		for prop in self._properties:
			self.properties[prop.name] = prop
		for key in kwargs:
			self.properties[key].set(kwargs[key])
		self.init()

	def init(self):
		pass

	def render(self):
		result = {
			'id': self.id,
			'children': [c.render() for c in self.children],
		}
		for prop in self.properties.values():
			result[prop.name] = prop.value
		return result

	def append(self, child):
		self.children.append(child)

	def remove(self, child):
		self.children.remove(child)


class UI (object):
	def __init__(self):
		pass

	@staticmethod
	def create(id, *args, **kwargs):
		for cls in UIElement.get_classes():
			if cls.id == id:
				return cls(*args, **kwargs)
		return UIElement(id=id, *args, **kwargs)

	def render(self):
		return self.root.render()


def p(prop, default=None):
	def decorator(cls):
		prop_obj = UIProperty(prop, value=default)
		if not hasattr(cls, '_properties'):
			cls._properties = []
		cls._properties.append(prop_obj)

		def get(self):
			return self.properties[prop].get()

		def set(self, value):
			return self.properties[prop].set(value)

		setattr(cls, prop, property(get, set))
		return cls
	return decorator


__all__ = ['UI', 'UIElement', 'p']