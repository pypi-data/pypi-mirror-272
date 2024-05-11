```python
"""PYTZEN is designed to sketch out data pipelines.
"""

import json
import sys
import importlib.util
import os
from datetime import datetime
from dataclasses import dataclass, field



DIR = os.getcwd()


def new_namespace(namespace: str):
    """
    Creates and returns a new namespace as a module, isolated from the 
    original pytzen package.

    This function dynamically imports the pytzen package, then creates a 
    new module object based on the pytzen specification. It sets the 
    newly created module's MetaType.NAMESPACE attribute to the provided 
    namespace string. The new namespace is also added to the 
    sys.modules dictionary, making it recognized as a legitimate 
    module.

    Args:
    namespace: The name of the new namespace to create. This name is 
        used to isolate the created module and its configurations from 
        other modules or namespaces.

    Returns:
    module: A new module object that represents the isolated namespace. 
        This module is a clone of the pytzen package, but with its 
        MetaType.NAMESPACE attribute set to the given namespace name, 
        allowing for isolated configuration and operation within this 
        new context.
    """

    pytzen = importlib.util.find_spec('pytzen')
    vars()[namespace] = importlib.util.module_from_spec(pytzen)
    pytzen.loader.exec_module(vars()[namespace])
    sys.modules[namespace] = vars()[namespace]
    vars()[namespace].MetaType.NAMESPACE = namespace

    return vars()[namespace]



class MetaType(type):
    """Metaclass for ProtoType class. It is responsible for adding the 
    meta_attr attribute to the class and initializing the ProtoType 
    class.

    Attributes:
    NAMESPACE: Class attribute set to the given namespace name.
    
    Methods:
    __new__: Adds the meta_attr attribute to the class.
    __call__: Initializes the ProtoType class.
    log: Adds a message to the log attribute.
    store: Adds a value to the store attribute.
    close: Closes the namespace and stores the data.
    """

    NAMESPACE: str = None
    def __new__(cls, name, bases, attrs) -> type:
        """Enriches a class with logging, data storage, and closure 
        capabilities.
    
        This method dynamically adds three methods to a class during its 
        creation: `log`, `store`, and `close`. These methods are 
        intended to provide standardized logging, data persistence, and 
        clean-up functionalities across different classes without the 
        need to redefine them in each class.
    
        Args:
        name (str): The name of the class being created. It's used 
            internally by Python during class creation and helps in 
            identifying the class in a human-readable form.
        bases (tuple): A tuple of the base classes from which the new 
            class inherits. This parameter defines the inheritance 
            chain, allowing the new class to inherit attributes and 
            methods from these base classes.
        attrs (dict): A dictionary of attributes and methods that the 
            new class will have. This includes both the methods defined 
            within the class body and those dynamically added or 
            modified during class creation.
    
        Returns:
        type: A new class object, augmented with the `log`, `store`, and 
            `close` methods, ready to be used to create instances that 
            have standardized mechanisms for logging, data handling, 
            and resource management.
        """

        attrs['log'] = cls.log
        attrs['store'] = cls.store
        attrs['close'] = cls.close
        new_cls = super().__new__(cls, name, bases, attrs)

        return new_cls
    

    def __call__(self, *args, **kwargs) -> object:
        """Initializes an instance of a derived class within a 
        prototype-based design.

        This method serves as a customized instantiation process for 
            classes following the Prototype pattern. The Prototype 
            pattern is a creational design pattern used in software 
            development when the type of objects to create is determined 
            by a prototypical instance, which is cloned to produce new 
            objects. This `__call__` method facilitates the 
            initialization of a derived class by first invoking the 
            initialization of the 'ProtoType' base class to ensure 
            that any setup required by the base class is completed 
            before the derived class's own initialization logic is 
            executed.

        Args:
        *args: Variable length argument list. These are positional 
            arguments passed to the class constructor during 
            instantiation. They allow the initialization of an instance 
            with specific values that could differ from one instance to 
            another.
        **kwargs: Arbitrary keyword arguments. These are passed to the 
            class constructor as named arguments. This mechanism 
            supports more explicit initialization of instances where 
            parameter names are specified, enhancing code readability 
            and flexibility.

        Returns:
        object: An instance of the derived class, properly initialized 
            and ready for use. This instance has been passed through the 
            initialization process of the 'ProtoType' base class and 
            then through any additional initialization logic defined in 
            the derived class itself.

        Note:
        This method explicitly calls the `__init__` method of the 
            'ProtoType' class to ensure that any foundational setup 
            provided by the 'ProtoType' is incorporated. It then 
            delegates further initialization to the `__call__` method of 
            the superclass, allowing for any additional constructor 
            logic specific to the derived class to be executed.
        """
        
        ProtoType.__init__(self)

        return super().__call__(*args, **kwargs)
    

    @classmethod
    def log(cls, message, stdout=True, write=True) -> None:
        """Records a log message with an optional display and storage 
        behavior.

        This method offers a flexible logging mechanism for classes 
        inheriting from the 'ProtoType'. It allows for the logging of 
        messages with a timestamp, enhancing debugging, monitoring, and 
        auditing capabilities. The method provides options to both 
        display the message to the standard output (such as a console) 
        and to store it in a structured log attribute for later 
        retrieval or analysis.

        Args:
        message (str): The log message to be processed. This could be 
            any textual information that needs to be logged, such as 
            debug information, errors, or operational messages.
        stdout (bool, optional): Controls whether the message is printed 
            to the standard output. If True, the message, along with its 
            timestamp, is displayed. This is useful for immediate 
            feedback during development or monitoring. Defaults to True.
        write (bool, optional): Determines if the message should be 
            stored. If True, the message is saved in the 
            'ProtoType.data.log' dictionary, keyed by its timestamp. 
            This facilitates historical logging and subsequent retrieval 
            for analysis or debugging purposes. Defaults to True.

        Returns:
        None: This method does not return a value. Its primary purpose 
            is the side effect of logging a message.

        Note:
        The method uses the 
            'datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")' function 
            to generate a string representation of the current 
            timestamp. This timestamp is used both as a prefix for 
            messages printed to the standard output and as the key for 
            storing messages in the log attribute, ensuring that each 
            logged message is uniquely identifiable and chronologically 
            ordered.
        """

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if write:
            ProtoType.data.log[timestamp] = message
        if stdout:
            print(f'{timestamp}: {message}')


    @classmethod
    def store(cls, name, value) -> None:
        """Stores a named value within the class's shared data store.

        This method facilitates a centralized mechanism for storing and 
        accessing data values associated with unique names within 
        classes inheriting from 'ProtoType'. It acts as a simple 
        key-value store, where each 'name' acts as a unique identifier 
        for the 'value' stored. This can be particularly useful for 
        managing configurations, shared resources, or stateful data 
        across instances of the class or between different class 
        methods.

        Args:
        name (str): The unique identifier for the value to be stored. 
            This name is used as a key in the data store, allowing for 
            the later retrieval of the value.
        value (any): The data to be stored under the given name. This 
            can be any type of data, including but not limited to 
            strings, numbers, lists, or dictionaries.

        Returns:
        None: This method does not return any value. Its purpose is to 
            modify the class's shared data store by adding or updating 
            the value associated with the specified name.

        Note:
        The method directly modifies the 'ProtoType.data.store' 
            dictionary, adding or updating the key-value pair where the 
            key is 'name' and the value is 'value'. If 'name' already 
            exists in the store, its associated value is updated; 
            otherwise, a new key-value pair is added. This approach 
            ensures that data can be dynamically stored and accessed by 
            any instance or class method of 'ProtoType' or its 
            derivatives, facilitating easy data sharing and management 
            within the class hierarchy.
        """

        ProtoType.data.store[name] = value
    

    @classmethod
    def close(cls) -> None:
        """Finalizes operations by persistently storing class data.

        This method is designed to be called after all instances of 
        derived classes have completed their tasks, marking the end of 
        the operational lifecycle. It serializes and saves the 
        accumulated data, including class structures, log messages, and 
        stored values, into JSON files. This ensures that the state and 
        activities of the class instances are preserved for future 
        analysis, debugging, or continuation of operations.

        The method aggregates data from three main components:
        - Class structures ('classes')
        - Log messages ('log')
        - Stored values ('store')

        Each component's data is serialized into a JSON file, named 
        according to the class's namespace and the type of data it 
        contains. This structured approach to data management 
        facilitates easy retrieval, analysis, and auditing of the 
        operation's history and state.

        Returns:
        None: This method does not return a value. It concludes its 
            execution by writing data to files, effectively persisting 
            the state of the application for future reference.

        Note:
        Before invoking this method, ensure that all necessary 
            operations by the derived classes are complete, as it marks 
            the termination of data logging and storage within the 
            current session. The method dynamically constructs file 
            paths using the 'namespace' specified in 
            'MetaType.NAMESPACE' and the predefined directory from the 
            'pytzen' module. It checks for the existence of data before 
            attempting to write to files, preventing the creation of 
            empty files and ensuring that only meaningful data is 
            stored.
        """

        namespace = MetaType.NAMESPACE
        pack = {
            f'{namespace}_dataclasses.json': ProtoType.data.classes,
            f'{namespace}_log.json': ProtoType.data.log,
            f'{namespace}_store.json': ProtoType.data.store,
        }
        for k, v in pack.items():
            if v:
                path = os.path.join(sys.modules['pytzen'].DIR, k)
                with open(path, 'w') as json_file:
                    json.dump(v, json_file, indent=4)



class ProtoType(metaclass=MetaType):
    """
    The `ProtoType` class serves as a foundational component in a 
    dynamic class creation and configuration management system, 
    leveraging a custom metaclass `MetaType` to control instantiation 
    behavior. It encapsulates common functionalities and data needed 
    across various derived classes, focusing on configuration and 
    pipeline management.

    This class is designed to store and manage essential pipeline 
    information, ensuring that each derived class has access to a 
    unified configuration and shared data structure for consistent 
    behavior across the application. It automates the process of 
    configuration file loading and the initialization of shared data 
    resources, facilitating a more modular and scalable development 
    approach.

    Module Attributes:
    DIR (str): A class-level attribute that specifies the output 
        directory path where the `config.json` file is expected to be 
        found. This path is utilized to locate and load the 
        configuration settings needed by instances of `ProtoType` or its 
        derived classes.

    Attributes:
    class_path (str): A string that holds the fully qualified name of 
        the class, including both the module and class name. This is 
        used for identification purposes in the shared data structure.
    config (dict): A dictionary loaded from a JSON configuration file 
        (`config.json`). This configuration is shared across all 
        instances and derived classes, providing a centralized set of 
        parameters for the application.
    data (SharedData): An instance of `SharedData`, a custom class 
        designed to hold shared data across all instances. It includes a 
        registry of classes with their attributes and methods, 
        facilitating introspection and dynamic behavior adjustments.

    Methods:
    __init__(self) -> None: Constructor method that initializes a new 
        instance of the `ProtoType` class. It sets up the `class_path`, 
        loads the configuration from a JSON file if not already loaded, 
        and initializes the shared data structure if it has not been set 
        up. This ensures that every instance has access to the necessary 
        configuration and shared data.
    __setattr__(self, key: str, value: Any) -> None: A custom attribute 
        setter method that is called whenever a new attribute is added 
        to an instance. It updates the shared data structure with the 
        new attribute, maintaining a dynamic record of instance 
        attributes and their types for introspection and management 
        purposes.

    Note:
    The `ProtoType` class and its dynamic behavior are heavily reliant 
        on the `MetaType` metaclass for instantiation control and the 
        setup of class-wide configurations and shared data. This design 
        promotes a flexible and efficient mechanism for managing class 
        instances and their configurations.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the `ProtoType` class, 
        orchestrated under the controlled instantiation behavior 
        enforced by the `MetaType` metaclass. This constructor is 
        pivotal for setting up the class identity and ensuring the 
        configuration and shared data structures are properly 
        initialized across derived classes.

        The initialization process includes:
        - Setting the `class_path` attribute with the fully qualified 
        name of the class, which uniquely identifies the class within 
        the shared data structure.
        - Loading the JSON configuration file (`config.json`) if it has 
        not been loaded already, storing the settings in a class-level 
        `config` attribute accessible to all instances.
        - Initializing a shared `data` attribute if it does not exist, 
        which acts as a central registry for all classes, storing their 
        attributes and methods for introspection and dynamic behavior 
        adjustments.

        This structured setup facilitates a unified configuration 
        environment and shared data access, enhancing modularity and 
        scalability in application development.

        Returns:
        None
        """
        self.class_path = f'{self.__module__}.{self.__name__}'

        if not hasattr(ProtoType, 'config'):
            path = os.path.join(sys.modules['pytzen'].DIR, 'config.json')
            with open(path, 'r') as json_file:
                config = json.load(json_file)
            ProtoType.config = type('ConfigurationFile', (), config)

        if not hasattr(ProtoType, 'data'):
            ProtoType.data = SharedData()
        ProtoType.data.classes[self.class_path] = {
            'attributes': {},
            'methods': [k for k, v in self.__dict__.items() 
                        if callable(v) and '__' not in k],
        }
    

    def __setattr__(self, key, value) -> None:
        """
        Overrides the default behavior for setting attributes to ensure 
        that every new attribute added to an instance of `ProtoType` or 
        its derived classes is registered in a shared data structure. 
        This method facilitates dynamic updates to the instance's state 
        and allows for centralized tracking of attributes across all 
        class instances.

        This method serves multiple purposes:
        - It adds the attribute directly to the instance, allowing 
        normal attribute functionality.
        - It updates the shared data structure (`ProtoType.data`) to 
        include the new attribute and its type, enhancing the dynamic 
        behavior of the class by making these attributes available for 
        introspection and management across the entire application.
        - It maintains a record of attribute names and their 
        corresponding types in a dictionary, facilitating easier access 
        and modification by other parts of the application, especially 
        for functionalities that rely on dynamic attribute manipulation.

        Args:
        key (str): The name of the attribute to be added or modified.
        value (Any): The value of the attribute to be set.

        Returns:
        None
        """

        setattr(ProtoType.data, key, value)
        attr_type = str(type(value).__name__)
        ProtoType.data.classes[self.class_path]\
            ['attributes'][key] = attr_type



@dataclass
class SharedData:
    """
    A data class for storing and managing shared pipeline information in 
    an immutable structure.

    This class encapsulates essential data used across different 
    components of a software application, specifically designed to 
    prevent unintended side effects by enforcing immutability once data 
    has been initially set. This ensures that the data remains 
    consistent and reliable throughout the lifecycle of the application, 
    particularly in concurrent or complex pipeline environments.

    Attributes:
    classes (dict): A dictionary storing references to classes used 
        within the pipeline. This may include class types, 
        configurations, and other metadata pertinent to the operation of 
        the pipeline.
    log (dict): A dictionary that aggregates logging information. This 
        can be utilized to track events, errors, or other significant 
        occurrences throughout the execution of the pipeline.
    store (dict): A dictionary used to store miscellaneous values that 
        need to be accessed by various components of the application. 
        This could include configuration settings, intermediate data, 
        and other operational parameters.

    Each dictionary defaults to an empty dictionary if not provided 
    during initialization.
    """
    classes: dict = field(default_factory=dict)
    log: dict = field(default_factory=dict)
    store: dict = field(default_factory=dict)
    

    def __setattr__(self, key, value) -> None:
        """
        Overrides the default attribute setting behavior specifically to 
        enforce immutability for attributes once they have been set. 
        This method is designed to prevent accidental changes to key 
        attributes that are crucial for the integrity and consistency of 
        shared data across various components of the application.

        This custom behavior serves the purpose of maintaining stability 
        and predictability in the shared data structure by:
        - Allowing the initial setting of attributes to ensure 
        flexibility during the setup phase.
        - Prohibiting the modification of attributes once they are set, 
        thus preventing inconsistencies and potential bugs that could 
        arise from dynamic changes to critical data during runtime.

        If an attempt is made to modify an existing attribute, an 
        `AttributeError` is raised with a clear message explaining that 
        the attribute cannot be changed.

        Args:
        key (str): The name of the attribute to be added or modified.
        value (Any): The value of the attribute to be set.

        Raises:
        AttributeError: If there is an attempt to modify an attribute 
            that has already been set, indicating that attributes should 
            be immutable once initialized.

        Returns:
        None
        """

        if hasattr(self, key):
            error = f"Attribute '{key}' already exists and cannot be changed."
            raise AttributeError(error)
        else:
            super().__setattr__(key, value)
```
