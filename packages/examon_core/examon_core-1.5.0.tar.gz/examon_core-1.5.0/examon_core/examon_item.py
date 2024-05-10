from .factories.item import ItemFactory
from .global_settings import ExamonGlobalSettings


def examon_item(
    internal_id=None,
    choices=None,
    choice_list=None,
    tags=None,
    hints=None,
    param1=None,
    repository=None,
    record_metrics=None,
    version=None,
    code_execution_driver_class=None,
    calc_standard_metrics_strategy=None,
    categorize_difficulty_strategy=None,
    unique_id_strategy=None,
):
    def inner_function(function):
        processed_question = ItemFactory.default_instance(
            code_execution_driver_class=code_execution_driver_class,
            calc_standard_metrics_strategy=calc_standard_metrics_strategy,
            categorize_difficulty_strategy=categorize_difficulty_strategy,
            unique_id_strategy=unique_id_strategy,
        ).build(
            function=function,
            internal_id=internal_id,
            choice_list=choices or choice_list,
            tags=tags,
            hints=hints,
            param1=param1,
            repository=(repository or ExamonGlobalSettings.repository),
            version=version or ExamonGlobalSettings.version,
            metrics=(record_metrics or ExamonGlobalSettings.record_metrics),
        )
        ExamonGlobalSettings.in_memory_db.add(processed_question)
        return function

    return inner_function
