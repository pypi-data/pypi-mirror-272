use parking_lot::RwLock;
use pyo3::prelude::*;

use crate::classes::base;
use crate::internal;

#[pyclass(extends=base::BaseCacheImpl, subclass, module = "cachebox._cachebox")]
pub struct LRUCache {
    pub inner: RwLock<internal::LRUCache<isize, base::KeyValuePair>>,
}

#[pymethods]
impl LRUCache {
    #[new]
    #[pyo3(signature=(maxsize, iterable=None, *, capacity=0))]
    fn __new__(
        py: Python<'_>,
        maxsize: usize,
        iterable: Option<PyObject>,
        capacity: usize,
    ) -> PyResult<(Self, base::BaseCacheImpl)> {
        let (slf, base) = (
            LRUCache {
                inner: RwLock::new(internal::LRUCache::new(maxsize, capacity)),
            },
            base::BaseCacheImpl {},
        );

        if let Some(x) = iterable {
            slf.update(py, x)?;
        }

        Ok((slf, base))
    }

    #[getter]
    fn maxsize(&self) -> usize {
        self.inner.read().maxsize
    }

    fn __len__(&self) -> usize {
        self.inner.read().len()
    }

    fn __sizeof__(&self) -> usize {
        let read = self.inner.read();
        let cap = read.capacity();

        (cap * base::ISIZE_MEMORY_SIZE)
            + (cap * base::PYOBJECT_MEMORY_SIZE)
            + (read.order_capacity() * base::ISIZE_MEMORY_SIZE)
            + base::ISIZE_MEMORY_SIZE
    }

    fn __bool__(&self) -> bool {
        !self.inner.read().is_empty()
    }

    fn __setitem__(&self, py: Python<'_>, key: PyObject, value: PyObject) -> PyResult<()> {
        let hash = pyany_to_hash!(key, py)?;
        self.inner
            .write()
            .insert(hash, base::KeyValuePair(key, value))
    }

    fn insert(&self, py: Python<'_>, key: PyObject, value: PyObject) -> PyResult<()> {
        self.__setitem__(py, key, value)
    }

    fn __getitem__(&self, py: Python<'_>, key: PyObject) -> PyResult<PyObject> {
        let hash = pyany_to_hash!(key, py)?;

        match self.inner.write().get(&hash) {
            Some(x) => Ok(x.1.clone()),
            None => Err(pyo3::exceptions::PyKeyError::new_err(key)),
        }
    }

    #[pyo3(signature=(key, default=None))]
    fn get(&self, py: Python<'_>, key: PyObject, default: Option<PyObject>) -> PyResult<PyObject> {
        let hash = pyany_to_hash!(key, py)?;

        match self.inner.write().get(&hash) {
            Some(val) => Ok(val.1.clone()),
            None => Ok(default.unwrap_or_else(|| py.None())),
        }
    }

    fn __delitem__(&self, py: Python<'_>, key: PyObject) -> PyResult<()> {
        let hash = pyany_to_hash!(key, py)?;

        match self.inner.write().remove(&hash) {
            Some(_) => Ok(()),
            None => Err(pyo3::exceptions::PyKeyError::new_err(key)),
        }
    }

    fn __contains__(&self, py: Python<'_>, key: PyObject) -> PyResult<bool> {
        let hash = pyany_to_hash!(key, py)?;
        Ok(self.inner.read().contains_key(&hash))
    }

    fn __eq__(&self, other: &Self) -> bool {
        let map1 = self.inner.read();
        let map2 = other.inner.read();
        map1.eq(&map2)
    }

    fn __ne__(&self, other: &Self) -> bool {
        let map1 = self.inner.read();
        let map2 = other.inner.read();
        map1.ne(&map2)
    }

    fn __iter__(slf: PyRef<'_, Self>) -> PyResult<Py<base::VecOneValueIterator>> {
        let read = slf.inner.read();
        let view: Vec<PyObject> = read
            .sorted_keys()
            .map(|x| read.fast_get(x).unwrap().0.clone())
            .collect();

        let iter = base::VecOneValueIterator {
            view: view.into_iter(),
        };

        Py::new(slf.py(), iter)
    }

    fn keys(slf: PyRef<'_, Self>) -> PyResult<Py<base::VecOneValueIterator>> {
        let read = slf.inner.read();
        let view: Vec<PyObject> = read
            .sorted_keys()
            .map(|x| read.fast_get(x).unwrap().0.clone())
            .collect();

        let iter = base::VecOneValueIterator {
            view: view.into_iter(),
        };

        Py::new(slf.py(), iter)
    }

    fn values(slf: PyRef<'_, Self>) -> PyResult<Py<base::VecOneValueIterator>> {
        let read = slf.inner.read();
        let view: Vec<PyObject> = read
            .sorted_keys()
            .map(|x| read.fast_get(x).unwrap().1.clone())
            .collect();

        let iter = base::VecOneValueIterator {
            view: view.into_iter(),
        };

        Py::new(slf.py(), iter)
    }

    fn items(slf: PyRef<'_, Self>) -> PyResult<Py<base::VecItemsIterator>> {
        let read = slf.inner.read();
        let view: Vec<(PyObject, PyObject)> = read
            .sorted_keys()
            .map(|x| {
                let val = read.fast_get(x).unwrap();
                (val.0.clone(), val.1.clone())
            })
            .collect();

        let iter = base::VecItemsIterator {
            view: view.into_iter(),
        };

        Py::new(slf.py(), iter)
    }

    fn __repr__(&self) -> String {
        let read = self.inner.read();
        if read.maxsize == 0 {
            format!("LRUCache({}, capacity={})", read.len(), read.capacity())
        } else {
            format!(
                "LRUCache({} / {}, capacity={})",
                read.len(),
                read.maxsize,
                read.capacity()
            )
        }
    }

    fn capacity(&self) -> usize {
        self.inner.read().capacity()
    }

    #[pyo3(signature=(*, reuse=false))]
    fn clear(&self, reuse: bool) {
        self.inner.write().clear(reuse);
    }

    #[pyo3(signature=(key, default=None))]
    fn pop(&self, py: Python<'_>, key: PyObject, default: Option<PyObject>) -> PyResult<PyObject> {
        let hash = pyany_to_hash!(key, py)?;

        match self.inner.write().remove(&hash) {
            Some(x) => Ok(x.1),
            None => Ok(default.unwrap_or_else(|| py.None())),
        }
    }

    #[pyo3(signature=(key, default=None))]
    fn setdefault(
        &self,
        py: Python<'_>,
        key: PyObject,
        default: Option<PyObject>,
    ) -> PyResult<PyObject> {
        let hash = pyany_to_hash!(key, py)?;
        let default_val = default.unwrap_or_else(|| py.None());

        match self
            .inner
            .write()
            .setdefault(hash, base::KeyValuePair(key, default_val))
        {
            Ok(x) => Ok(x.1),
            Err(s) => Err(s),
        }
    }

    fn popitem(&self) -> PyResult<(PyObject, PyObject)> {
        match self.inner.write().popitem() {
            Some(val) => Ok((val.0, val.1)),
            None => Err(pyo3::exceptions::PyKeyError::new_err(())),
        }
    }

    fn drain(&self, n: usize) -> usize {
        self.inner.write().drain(n)
    }

    fn update(&self, py: Python<'_>, iterable: PyObject) -> PyResult<()> {
        let obj = iterable.bind(py);

        if obj.is_instance_of::<pyo3::types::PyDict>() {
            let dict = obj.downcast::<pyo3::types::PyDict>()?;

            self.inner.write().update(dict.iter().map(|(key, val)| {
                Ok::<(isize, base::KeyValuePair), PyErr>((
                    unsafe { key.hash().unwrap_unchecked() },
                    base::KeyValuePair(key.into(), val.into()),
                ))
            }))?;
        } else {
            let iter = obj.iter()?;

            self.inner.write().update(iter.map(|key| {
                let items: (&PyAny, &PyAny) = key?.extract()?;
                let hash = items.0.hash()?;

                Ok::<(isize, base::KeyValuePair), PyErr>((
                    hash,
                    base::KeyValuePair(items.0.into(), items.1.into()),
                ))
            }))?;
        }

        Ok(())
    }

    fn shrink_to_fit(&self) {
        self.inner.write().shrink_to_fit();
    }

    fn __traverse__(&self, visit: pyo3::PyVisit<'_>) -> Result<(), pyo3::PyTraverseError> {
        for value in self.inner.read().values() {
            visit.call(&value.0)?;
            visit.call(&value.1)?;
        }
        Ok(())
    }

    fn __clear__(&self) {
        self.inner.write().clear(false);
    }

    fn least_recently_used(&self) -> Option<PyObject> {
        let read = self.inner.read();
        Some(read.fast_get(read.least_recently_used()?)?.0.clone())
    }

    fn most_recently_used(&self) -> Option<PyObject> {
        let read = self.inner.read();
        Some(read.fast_get(read.most_recently_used()?)?.0.clone())
    }
}
