use parking_lot::RwLock;
use pyo3::prelude::*;

use crate::classes::base;
use crate::internal;

#[pyclass(extends=base::BaseCacheImpl, subclass, module = "cachebox._cachebox")]
pub struct RRCache {
    pub inner: RwLock<internal::RRCache<isize, base::KeyValuePair>>,
}

#[pymethods]
impl RRCache {
    #[new]
    #[pyo3(signature=(maxsize, iterable=None, *, capacity=0))]
    fn __new__(
        py: Python<'_>,
        maxsize: usize,
        iterable: Option<PyObject>,
        capacity: usize,
    ) -> PyResult<(Self, base::BaseCacheImpl)> {
        let (slf, base) = (
            RRCache {
                inner: RwLock::new(internal::RRCache::new(maxsize, capacity)),
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
        self.inner.read().parent.maxsize
    }

    fn __len__(&self) -> usize {
        self.inner.read().parent.len()
    }

    fn __sizeof__(&self) -> usize {
        let cap = self.inner.read().parent.capacity();

        cap * base::ISIZE_MEMORY_SIZE + cap * base::PYOBJECT_MEMORY_SIZE + base::ISIZE_MEMORY_SIZE
    }

    fn __bool__(&self) -> bool {
        !self.inner.read().parent.is_empty()
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

        match self.inner.read().parent.get(&hash) {
            Some(x) => Ok(x.1.clone()),
            None => Err(pyo3::exceptions::PyKeyError::new_err(key)),
        }
    }

    #[pyo3(signature=(key, default=None))]
    fn get(&self, py: Python<'_>, key: PyObject, default: Option<PyObject>) -> PyResult<PyObject> {
        let hash = pyany_to_hash!(key, py)?;

        match self.inner.read().parent.get(&hash) {
            Some(val) => Ok(val.1.clone()),
            None => Ok(default.unwrap_or_else(|| py.None())),
        }
    }

    fn __delitem__(&self, py: Python<'_>, key: PyObject) -> PyResult<()> {
        let hash = pyany_to_hash!(key, py)?;

        match self.inner.write().parent.remove(&hash) {
            Some(_) => Ok(()),
            None => Err(pyo3::exceptions::PyKeyError::new_err(key)),
        }
    }

    fn __contains__(&self, py: Python<'_>, key: PyObject) -> PyResult<bool> {
        let hash = pyany_to_hash!(key, py)?;
        Ok(self.inner.read().parent.contains_key(&hash))
    }

    fn __eq__(&self, other: &Self) -> bool {
        let map1 = self.inner.read();
        let map2 = other.inner.read();

        map1.parent.maxsize == map2.parent.maxsize
            && map1.parent.keys().all(|x| map2.parent.contains_key(x))
    }

    fn __ne__(&self, other: &Self) -> bool {
        let map1 = self.inner.read();
        let map2 = other.inner.read();

        map1.parent.maxsize != map2.parent.maxsize
            || map1.parent.keys().all(|x| !map2.parent.contains_key(x))
    }

    fn __iter__(slf: PyRef<'_, Self>) -> PyResult<Py<base::VecOneValueIterator>> {
        let view: Vec<PyObject> = slf
            .inner
            .read()
            .parent
            .values()
            .map(|x| x.0.clone())
            .collect();

        let iter = base::VecOneValueIterator {
            view: view.into_iter(),
        };

        Py::new(slf.py(), iter)
    }

    fn keys(slf: PyRef<'_, Self>) -> PyResult<Py<base::VecOneValueIterator>> {
        let view: Vec<PyObject> = slf
            .inner
            .read()
            .parent
            .values()
            .map(|x| x.0.clone())
            .collect();

        let iter = base::VecOneValueIterator {
            view: view.into_iter(),
        };

        Py::new(slf.py(), iter)
    }

    fn values(slf: PyRef<'_, Self>) -> PyResult<Py<base::VecOneValueIterator>> {
        let view: Vec<PyObject> = slf
            .inner
            .read()
            .parent
            .values()
            .map(|x| x.1.clone())
            .collect();

        let iter = base::VecOneValueIterator {
            view: view.into_iter(),
        };

        Py::new(slf.py(), iter)
    }

    fn items(slf: PyRef<'_, Self>) -> PyResult<Py<base::VecItemsIterator>> {
        let view: Vec<(PyObject, PyObject)> = slf
            .inner
            .read()
            .parent
            .values()
            .map(|x| (x.0.clone(), x.1.clone()))
            .collect();

        let iter = base::VecItemsIterator {
            view: view.into_iter(),
        };

        Py::new(slf.py(), iter)
    }

    fn __repr__(&self) -> String {
        let read = self.inner.read();
        if read.parent.maxsize == 0 {
            format!(
                "RRCache({}, capacity={})",
                read.parent.len(),
                read.parent.capacity()
            )
        } else {
            format!(
                "RRCache({} / {}, capacity={})",
                read.parent.len(),
                read.parent.maxsize,
                read.parent.capacity()
            )
        }
    }

    fn capacity(&self) -> usize {
        self.inner.read().parent.capacity()
    }

    #[pyo3(signature=(*, reuse=false))]
    fn clear(&self, reuse: bool) {
        self.inner.write().parent.clear(reuse);
    }

    #[pyo3(signature=(key, default=None))]
    fn pop(&self, py: Python<'_>, key: PyObject, default: Option<PyObject>) -> PyResult<PyObject> {
        let hash = pyany_to_hash!(key, py)?;

        match self.inner.write().parent.remove(&hash) {
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
        self.inner.write().parent.shrink_to_fit();
    }

    fn __traverse__(&self, visit: pyo3::PyVisit<'_>) -> Result<(), pyo3::PyTraverseError> {
        for value in self.inner.read().parent.values() {
            visit.call(&value.0)?;
            visit.call(&value.1)?;
        }
        Ok(())
    }

    fn __clear__(&self) {
        self.inner.write().parent.clear(false);
    }
}
