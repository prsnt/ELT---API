from typing import List, Optional
from typing import Union
from pydantic import BaseModel
import mysql.connector
from fastapi import FastAPI, Query

# Connect to your MySQL database
db_connection = mysql.connector.connect(
        host='localhost',
    user='prashant',
    password='pwd@123',
    database='elt_db'
)

# Create a cursor object
cursor = db_connection.cursor()
cursor2 = db_connection.cursor()

app = FastAPI()


class CategoryModel(BaseModel):
    cat_id: Union[int, None]
    cat_name: Union[str, None]


class TopicModel(BaseModel):
    topic_id: Union[int, None]
    topic_area: Union[str, None]


class DeveloperModel(BaseModel):
    developer_id: Union[int, None]
    developer_name: Union[str, None]


class TypeELTModel(BaseModel):
    elt_type_id: Union[int, None]
    elt_type_name: Union[str, None]


class CountryModel(BaseModel):
    country_id: Union[int, None]
    country_name: Union[str, None]


class LanguageModel(BaseModel):
    language_id: Union[int, None]
    language_name: Union[str, None]


class OccupationModel(BaseModel):
    occupation_id: Union[int, None]
    occupation_name: Union[str, None]


class TasksModel(BaseModel):
    task_id: Union[int, None]
    task_name: Union[str, None]


class OSHTopicModel(BaseModel):
    osh_topic_id: Union[int, None]
    osh_topic_name: Union[str, None]


class HardwareModel(BaseModel):
    hardware_id: Union[int, None]
    hardware_name: Union[str, None]


class ErrorModel(BaseModel):
    code: int
    message: str


class ProductModelResponse(BaseModel):
    product_id: int
    name: str


class ProductModel(BaseModel):
    product_id: int
    name: str
    website: str
    description: str
    payment_type: str
    Date_of_Release_and_Version_Number: Optional[str]
    Certification_accreditation_for_completion: Optional[str]
    Duration_min: Optional[str]
    category: List[CategoryModel]
    topic: List[TopicModel]
    developers: List[DeveloperModel]
    type_of_elt: List[TypeELTModel]
    country: List[CountryModel]
    language: List[LanguageModel]
    occupation: List[OccupationModel]
    tasks: List[TasksModel]
    osh_topics: List[OSHTopicModel]
    hardware: List[HardwareModel]


class BaseProductResponse(BaseModel):
    success: int
    message: str
    error: Optional[ErrorModel]
    data: List[ProductModel]


class BaseSearchTopicResponse(BaseModel):
    success: int
    message: str
    error: Optional[ErrorModel]
    topics: List[TopicModel]
    names: List[ProductModelResponse]


class BaseFilterResponse(BaseModel):
    success: int
    message: str
    error: Optional[ErrorModel]
    category: List[CategoryModel]
    topics: List[TopicModel]
    developers: List[DeveloperModel]
    typeElts: List[TypeELTModel]
    languages: List[LanguageModel]


class BaseTopicResponse(BaseModel):
    success: int
    message: str
    error: Optional[ErrorModel]
    data: List[TopicModel]


class BaseTypeELTResponse(BaseModel):
    success: int
    message: str
    error: Optional[ErrorModel]
    data: List[TypeELTModel]


class BaseDeveloperResponse(BaseModel):
    success: int
    message: str
    error: Optional[ErrorModel]
    data: List[DeveloperModel]


class BaseCountryResponse(BaseModel):
    success: int
    message: str
    error: Optional[ErrorModel]
    data: List[CountryModel]


class BaseLanguageResponse(BaseModel):
    success: int
    message: str
    error: Optional[ErrorModel]
    data: List[LanguageModel]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/getFilters", response_model=BaseFilterResponse)
async def getFilters():
    queryCategory = "SELECT * from category_tbl"
    cursor.execute(queryCategory)
    result_Category = cursor.fetchall()

    queryTopics = "SELECT * from topicarea_tbl"
    cursor.execute(queryTopics)
    result_Topic = cursor.fetchall()

    queryELTtypes = "SELECT * from elt_types_tbl"
    cursor.execute(queryELTtypes)
    result_ELT = cursor.fetchall()

    queryDeveloper = "SELECT * from developer_tbl"
    cursor.execute(queryDeveloper)
    result_Developer = cursor.fetchall()

    queryLanguage = "SELECT * from language_tbl"
    cursor.execute(queryLanguage)
    result_Language = cursor.fetchall()

    categories = []
    topics = []
    typeElts = []
    developers = []
    languages = []

    if queryCategory:
        for (cat_id, cat_name, cat_name_fold) in result_Category:
            categories.append(CategoryModel(cat_id=cat_id, cat_name=cat_name))

    if queryTopics:
        for (topic_id, topic_area, topic_area_fold) in result_Topic:
            topics.append(TopicModel(topic_id=topic_id, topic_area=topic_area))

    if queryELTtypes:
        for (elt_id, elt_name, elt_name_fold) in result_ELT:
            typeElts.append(TypeELTModel(elt_type_id=elt_id, elt_type_name=elt_name))

    if queryDeveloper:
        for (developer_id, developer_name, developer_name_fold) in result_Developer:
            developers.append(DeveloperModel(developer_id=developer_id, developer_name=developer_name))

    if queryLanguage:
        for (language_id, language_name, language_name_fold) in result_Language:
            languages.append(LanguageModel(language_id=language_id, language_name=language_name))

    # else:
    #     errorModel = ErrorModel(code=10, message="No Records Found!")
    #     responseModel = BaseProductResponse(success=0, message="Something went wrong!", error=errorModel,
    #                                         data=categories)
    #     print("No Records Found!")

    responseModel = BaseFilterResponse(success=1, message=f"Records Fetched", error=None,
                                       category=categories, topics=topics, developers=developers, typeElts=typeElts,
                                       languages=languages)

    return responseModel


@app.get("/getProducts", response_model=BaseProductResponse)
async def getProducts(page_number: int = Query(default=1, description="Page number", ge=1),
                      page_size: int = Query(default=10, description="Items per page", le=100),
                      cat_id: Optional[str] = Query(None, description="Category ID"),
                      product_id: int = Query(None, description="Product ID"),
                      topic_id: Optional[str] = Query(None, description="Topic ID"),
                      type_elt_id: Optional[str] = Query(None, description="Type of ELT ID"),
                      developer_id: Optional[str] = Query(None, description="Developer ID"),
                      country_id: Optional[str] = Query(None, description="Country ID"),
                      language_id: Optional[str] = Query(None, description="Language ID"),
                      payment_type: Optional[str] = Query(None, description="Payment Type")):
    # Calculate offset and limit for pagination
    global query, category_filter, responseModel
    start_row = (page_number - 1) * page_size + 1
    end_row = page_number * page_size

    # count_of_topic = topic_id.count(",") + 1

    category_filter = " WHERE 1=1"

    if cat_id:
        category_filter += f" AND t3.cat_id IN ({cat_id})"

    if product_id:
        category_filter += f" AND t1.product_id = {product_id}"

    if topic_id:
        category_filter += f" AND tat.topic_id IN ({topic_id})"

    if type_elt_id:
        category_filter += f" AND et.elt_type_id IN ({type_elt_id})"

    if developer_id:
        category_filter += f" AND dev.developer_id IN ({developer_id})"

    if country_id:
        category_filter += f" AND ct.country_id IN ({country_id})"

    if language_id:
        category_filter += f" AND lt.language_id IN ({language_id})"

    if payment_type:
        category_filter += f" AND t1.Free_Paid = '{payment_type}'"

    category_filter += " GROUP BY t1.product_id"

    if cat_id:
        count_of_cat = cat_id.count(",") + 1
        if category_filter.__contains__("HAVING"):
            category_filter += f" AND COUNT(DISTINCT t3.cat_id) = {count_of_cat}"
        else:
            category_filter += f" HAVING COUNT(DISTINCT t3.cat_id) = {count_of_cat}"

    if topic_id:
        count_of_topic = topic_id.count(",") + 1
        if category_filter.__contains__("HAVING"):
            category_filter += f" AND COUNT(DISTINCT tat.topic_id) = {count_of_topic}"
        else:
            category_filter += f" HAVING COUNT(DISTINCT tat.topic_id) = {count_of_topic}"

    if type_elt_id:
        count_of_ELT = type_elt_id.count(",") + 1
        if category_filter.__contains__("HAVING"):
            category_filter += f" AND COUNT(DISTINCT et.elt_type_id) = {count_of_ELT}"
        else:
            category_filter += f" HAVING COUNT(DISTINCT et.elt_type_id) = {count_of_ELT}"

    if developer_id:
        count_of_developer = developer_id.count(",") + 1
        if category_filter.__contains__("HAVING"):
            category_filter += f" AND COUNT(DISTINCT dev.developer_id) = {count_of_developer}"
        else:
            category_filter += f" HAVING COUNT(DISTINCT dev.developer_id) = {count_of_developer}"

    if country_id:
        count_of_country = country_id.count(",") + 1
        if category_filter.__contains__("HAVING"):
            category_filter += f" AND COUNT(DISTINCT ct.country_id) = {count_of_country}"
        else:
            category_filter += f" HAVING COUNT(DISTINCT ct.country_id) = {count_of_country}"

    if language_id:
        count_of_language = language_id.count(",") + 1
        if category_filter.__contains__("HAVING"):
            category_filter += f" AND COUNT(DISTINCT lt.language_id) = {count_of_language}"
        else:
            category_filter += f" HAVING COUNT(DISTINCT lt.language_id) = {count_of_language}"

    category_filter += ') AS t1 '

    query = (
        "SELECT DISTINCT t1.product_id,t1.Name_of_OSH_related_ELT,t1.Website,t1.Description_of_technology,t1.Free_Paid,t1.Date_of_Release_and_Version_Number,t1.Certification_accreditation_for_completion,t1.Duration_min,t3.cat_id,t3.cat_name,tat.topic_id,"
        "tat.topic_area,dev.developer_id,dev.developer_name,et.elt_type_id,et.elt_type_name,ct.country_id,"
        "ct.country_name,lt.language_id,lt.language_name,ot.occupation_id,ot.occupation_name,tt.task_id,"
        "tt.task_name,ott.osh_topic_id,ott.osh_topic_name,ht.hardware_id,ht.hardware_name"
        " FROM (SELECT t1.product_id,t1.Name_of_OSH_related_ELT,t1.Website,t1.Description_of_technology,t1.Free_Paid,t1.Date_of_Release_and_Version_Number,t1.Certification_accreditation_for_completion,t1.Duration_min, ROW_NUMBER()"
        " OVER (ORDER BY t1.product_id) AS row_num FROM elt_clean_extraction t1"
        " LEFT JOIN product_category as t2 on t2.product_id = t1.product_id"
        " LEFT JOIN category_tbl as t3 on t3.cat_id = t2.category_id"
        " LEFT JOIN product_topic AS pt ON pt.product_id = t1.product_id"
        " LEFT JOIN topicarea_tbl AS tat ON tat.topic_id = pt.topic_id"
        " LEFT JOIN product_developer AS pd ON pd.product_id = t1.product_id"
        " LEFT JOIN developer_tbl AS dev ON dev.developer_id = pd.developer_id"
        " LEFT JOIN product_elt AS pe ON pe.product_id = t1.product_id "
        " LEFT JOIN elt_types_tbl AS et ON et.elt_type_id = pe.elt_id"
        " LEFT JOIN product_country AS pc ON pc.product_id = t1.product_id"
        " LEFT JOIN country_tbl AS ct ON ct.country_id = pc.country_id"
        " LEFT JOIN product_language AS pl ON pl.product_id = t1.product_id"
        " LEFT JOIN language_tbl AS lt ON lt.language_id = pl.language_id"
        " LEFT JOIN product_occupation AS po ON po.product_id = t1.product_id"
        " LEFT JOIN occupation_tbl AS ot ON ot.occupation_id = po.occupation_id"
        " LEFT JOIN product_task AS ptk ON ptk.product_id = t1.product_id"
        " LEFT JOIN tasks_tbl AS tt ON tt.task_id = ptk.task_id"
        " LEFT JOIN product_oshtopic AS pot ON pot.product_id = t1.product_id"
        " LEFT JOIN osh_topics_tbl AS ott ON ott.osh_topic_id = pot.osh_topic_id"
        " LEFT JOIN product_hardware AS ph ON ph.product_id = t1.product_id"
        " LEFT JOIN hardwares_tbl AS ht ON ht.hardware_id = ph.hardware_id"
        f"{category_filter}"
        " LEFT JOIN product_category AS t2 ON t2.product_id = t1.product_id"
        " LEFT JOIN category_tbl AS t3 ON t3.cat_id = t2.category_id"
        " LEFT JOIN product_topic AS pt ON pt.product_id = t1.product_id"
        " LEFT JOIN topicarea_tbl AS tat ON tat.topic_id = pt.topic_id"
        " LEFT JOIN product_developer AS pd ON pd.product_id = t1.product_id "
        " LEFT JOIN developer_tbl AS dev ON dev.developer_id = pd.developer_id"
        " LEFT JOIN product_elt AS pe ON pe.product_id = t1.product_id "
        " LEFT JOIN elt_types_tbl AS et ON et.elt_type_id = pe.elt_id"
        " LEFT JOIN product_country AS pc ON pc.product_id = t1.product_id "
        " LEFT JOIN country_tbl AS ct ON ct.country_id = pc.country_id"
        " LEFT JOIN product_language AS pl ON pl.product_id = t1.product_id "
        " LEFT JOIN language_tbl AS lt ON lt.language_id = pl.language_id"
        " LEFT JOIN product_occupation AS po ON po.product_id = t1.product_id "
        " LEFT JOIN occupation_tbl AS ot ON ot.occupation_id = po.occupation_id"
        " LEFT JOIN product_task AS ptk ON ptk.product_id = t1.product_id "
        " LEFT JOIN tasks_tbl AS tt ON tt.task_id = ptk.task_id"
        " LEFT JOIN product_oshtopic AS pot ON pot.product_id = t1.product_id "
        " LEFT JOIN osh_topics_tbl AS ott ON ott.osh_topic_id = pot.osh_topic_id"
        " LEFT JOIN product_hardware AS ph ON ph.product_id = t1.product_id "
        " LEFT JOIN hardwares_tbl AS ht ON ht.hardware_id = ph.hardware_id"
    )
    # query += f" AND t1.Free_Paid = 'Free'"
    query += f" WHERE t1.row_num BETWEEN {start_row} AND {end_row}"

    print(query)
    cursor.execute(query)
    results = cursor.fetchall()

    products = []
    productIds = []
    categories = []
    topics = []
    developers = []
    types = []
    countries = []
    languages = []
    occupations = []
    tasks = []
    oshTopics = []
    hardwares = []

    # print(results)
    print(start_row)
    print(end_row)

    if results:
        for (product_id, name, website, description, payment_type, Date_of_Release_and_Version_Number,
             Certification_accreditation_for_completion, Duration_min, cat_id, cat_name, topic_id, topic_name,
             developer_id, developer_name, type_id, type_name, country_id, country_name,
             language_id, language_name, occupation_id, occupation_name,
             task_id, task_name, oshtopic_id, oshtopic_name,
             hardware_id, hardware_name) in results:
            if product_id not in productIds:
                categories.clear()
                topics.clear()
                developers.clear()
                types.clear()
                countries.clear()
                languages.clear()
                occupations.clear()
                tasks.clear()
                oshTopics.clear()
                hardwares.clear()
                productIds.clear()
                productIds.append(product_id)
                categories.append(CategoryModel(cat_id=cat_id, cat_name=cat_name))
                topics.append(TopicModel(topic_id=topic_id, topic_area=topic_name))
                developers.append(DeveloperModel(developer_id=developer_id, developer_name=developer_name))
                types.append(TypeELTModel(elt_type_id=type_id, elt_type_name=type_name))
                countries.append(CountryModel(country_id=country_id, country_name=country_name))
                languages.append(LanguageModel(language_id=language_id, language_name=language_name))
                occupations.append(OccupationModel(occupation_id=occupation_id, occupation_name=occupation_name))
                tasks.append(TasksModel(task_id=task_id, task_name=task_name))
                oshTopics.append(OSHTopicModel(osh_topic_id=oshtopic_id, osh_topic_name=oshtopic_name))
                hardwares.append(HardwareModel(hardware_id=hardware_id, hardware_name=hardware_name))
                products.append(
                    ProductModel(product_id=product_id, name=name, website=website, description=description,
                                 payment_type=payment_type,
                                 Date_of_Release_and_Version_Number=Date_of_Release_and_Version_Number,
                                 Certification_accreditation_for_completion=Certification_accreditation_for_completion,
                                 Duration_min=Duration_min,
                                 category=categories,
                                 topic=topics, developers=developers, type_of_elt=types, country=countries,
                                 language=languages, occupation=occupations, tasks=tasks, osh_topics=oshTopics,
                                 hardware=hardwares))
            else:
                var = len(products) - 1
                if CategoryModel(cat_id=cat_id, cat_name=cat_name) not in categories:
                    categories.append(CategoryModel(cat_id=cat_id, cat_name=cat_name))
                if TopicModel(topic_id=topic_id, topic_area=topic_name) not in topics:
                    topics.append(TopicModel(topic_id=topic_id, topic_area=topic_name))
                if DeveloperModel(developer_id=developer_id, developer_name=developer_name) not in developers:
                    developers.append(DeveloperModel(developer_id=developer_id, developer_name=developer_name))
                if TypeELTModel(elt_type_id=type_id, elt_type_name=type_name) not in types:
                    types.append(TypeELTModel(elt_type_id=type_id, elt_type_name=type_name))
                if CountryModel(country_id=country_id, country_name=country_name) not in countries:
                    countries.append(CountryModel(country_id=country_id, country_name=country_name))
                if LanguageModel(language_id=language_id, language_name=language_name) not in languages:
                    languages.append(LanguageModel(language_id=language_id, language_name=language_name))
                if OccupationModel(occupation_id=occupation_id, occupation_name=occupation_name) not in occupations:
                    occupations.append(OccupationModel(occupation_id=occupation_id, occupation_name=occupation_name))
                if TasksModel(task_id=task_id, task_name=task_name) not in tasks:
                    tasks.append(TasksModel(task_id=task_id, task_name=task_name))
                if OSHTopicModel(osh_topic_id=oshtopic_id, osh_topic_name=oshtopic_name) not in oshTopics:
                    oshTopics.append(OSHTopicModel(osh_topic_id=oshtopic_id, osh_topic_name=oshtopic_name))
                if HardwareModel(hardware_id=hardware_id, hardware_name=hardware_name) not in hardwares:
                    hardwares.append(HardwareModel(hardware_id=hardware_id, hardware_name=hardware_name))

                products[var] = ProductModel(product_id=product_id, name=name, website=website, description=description,
                                             payment_type=payment_type,
                                             Date_of_Release_and_Version_Number=Date_of_Release_and_Version_Number,
                                             Certification_accreditation_for_completion=Certification_accreditation_for_completion,
                                             Duration_min=Duration_min,
                                             category=categories,
                                             topic=topics, developers=developers, type_of_elt=types, country=countries,
                                             language=languages, occupation=occupations, tasks=tasks,
                                             osh_topics=oshTopics,
                                             hardware=hardwares)
        responseModel = BaseProductResponse(success=1, message=f"{len(products)} records found", error=None,
                                            data=products)
    else:
        errorModel = ErrorModel(code=10, message="No Records Found!")
        responseModel = BaseProductResponse(success=0, message="Something went wrong!", error=errorModel, data=products)
        print("No Records Found!")
    return responseModel


@app.get("/search_topic_and_name", response_model=BaseSearchTopicResponse)
async def search_topic_and_name(search_text: str = Query(None, description="Search Text")):
    query_topics = f"SELECT topic_id, topic_area FROM topicarea_tbl WHERE topic_area like '{search_text}%'"
    query_names = f"SELECT product_id, Name_of_OSH_related_ELT FROM elt_clean_extraction WHERE Name_of_OSH_related_ELT like '{search_text}%'"
    print(query_topics)
    print(query_names)

    cursor.execute(query_topics)
    results_topics = cursor.fetchall()

    cursor.execute(query_names)
    results_names = cursor.fetchall()

    topics = []
    products = []

    if results_names or results_topics:
        for (product_id, Name_of_OSH_related_ELT) in results_names:
            products.append(ProductModelResponse(product_id=product_id, name=Name_of_OSH_related_ELT))

        for (topic_id, topic_area) in results_topics:
            topics.append(TopicModel(topic_id=topic_id, topic_area=topic_area))

        responseModel = BaseSearchTopicResponse(success=1, message=f"records found", error=None,
                                                topics=topics, names=products)
    else:
        errorModel = ErrorModel(code=10, message="No Records Found!")
        responseModel = BaseSearchTopicResponse(success=0, message="Something went wrong!", error=errorModel,
                                                topics=topics, names=products)
        print("No Records Found!")
    return responseModel


# dummy response
@app.get("/getallProducts")
async def get_all_products():
    return {
        "response": "success",
        "data": [{
            "product_id": 12,
            "Name_of_OSH_related_ELT": "3M Fall Protection Harness Inspection",
            "Website": "https://www.3m.com/3M/en_US/worker-health-safety-us/3m-ppe-training/virtual-reality/#",
            "Free_Paid": "Paid",
            "Description_of_technology": "Trainees will learn how to inspect a harness and be challenged to identify four defects in two minutes. Play through the VR scenario multiple times to build and reinforce knowledge by encountering different defects each time.",
            "Duration_min": "20 Mins",
            "Category": [{
                "cat_id": 1,
                "cat_name": "Construction"
            },
                {
                    "cat_id": 2,
                    "cat_name": "Industrial"
                }],
            "Key_Topic_Area": [{
                "topic_id": 1,
                "topic_area": "Fall Safety"
            },
                {
                    "topic_id": 2,
                    "topic_area": "Fall Safety"
                }],
            "Developers_Distributor": [{
                "developer_id": 1,
                "developer_name": "Fall Safety"
            },
                {
                    "developer_id": 2,
                    "developer_name": "Fall Safety"
                }],
            "Type_of_ELT": [{
                "elt_type_id": 1,
                "elt_type_name": "Fall Safety"
            },
                {
                    "elt_type_id": 2,
                    "elt_type_name": "Fall Safety"
                }],
            "Country_Head_Quarters": [{
                "country_id": 1,
                "country_name": "Fall Safety"
            },
                {
                    "country_id": 2,
                    "country_name": "Fall Safety"
                }],
            "Language": [{
                "language_id": 1,
                "language_name": "Fall Safety"
            },
                {
                    "language_id": 2,
                    "language_name": "Fall Safety"
                }],
            "Skilled_Trade_Occupation": [{
                "occupation_id": 1,
                "occupation_name": "Fall Safety"
            },
                {
                    "occupation_id": 2,
                    "occupation_name": "Fall Safety"
                }],
            "Tasks_Topics": [{
                "task_id": 1,
                "task_name": "Fall Safety"
            },
                {
                    "task_id": 2,
                    "task_name": "Fall Safety"
                }],
            "OSH_Topics": [{
                "osh_topic_id": 1,
                "osh_topic_name": "Fall Safety"
            },
                {
                    "osh_topic_id": 2,
                    "osh_topic_name": "Fall Safety"
                }],
            "Hardware_Options_for_ELT": [{
                "hardware_id": 1,
                "hardware_name": "Fall Safety"
            },
                {
                    "hardware_id": 2,
                    "hardware_name": "Fall Safety"
                }],
        }, {
            "product_id": 12,
            "Name_of_OSH_related_ELT": "3M Fall Protection Harness Inspection",
            "Website": "https://www.3m.com/3M/en_US/worker-health-safety-us/3m-ppe-training/virtual-reality/#",
            "Free_Paid": "Paid",
            "Description_of_technology": "Trainees will learn how to inspect a harness and be challenged to identify four defects in two minutes. Play through the VR scenario multiple times to build and reinforce knowledge by encountering different defects each time.",
            "Duration_min": "20 Mins",
            "Category": [{
                "cat_id": 1,
                "cat_name": "Construction"
            },
                {
                    "cat_id": 2,
                    "cat_name": "Industrial"
                }],
            "Key_Topic_Area": [{
                "topic_id": 1,
                "topic_area": "Fall Safety"
            },
                {
                    "topic_id": 2,
                    "topic_area": "Fall Safety"
                }],
            "Developers_Distributor": [{
                "developer_id": 1,
                "developer_name": "Fall Safety"
            },
                {
                    "developer_id": 2,
                    "developer_name": "Fall Safety"
                }],
            "Type_of_ELT": [{
                "elt_type_id": 1,
                "elt_type_name": "Fall Safety"
            },
                {
                    "elt_type_id": 2,
                    "elt_type_name": "Fall Safety"
                }],
            "Country_Head_Quarters": [{
                "country_id": 1,
                "country_name": "Fall Safety"
            },
                {
                    "country_id": 2,
                    "country_name": "Fall Safety"
                }],
            "Language": [{
                "language_id": 1,
                "language_name": "Fall Safety"
            },
                {
                    "language_id": 2,
                    "language_name": "Fall Safety"
                }],
            "Skilled_Trade_Occupation": [{
                "occupation_id": 1,
                "occupation_name": "Fall Safety"
            },
                {
                    "occupation_id": 2,
                    "occupation_name": "Fall Safety"
                }],
            "Tasks_Topics": [{
                "task_id": 1,
                "task_name": "Fall Safety"
            },
                {
                    "task_id": 2,
                    "task_name": "Fall Safety"
                }],
            "OSH_Topics": [{
                "osh_topic_id": 1,
                "osh_topic_name": "Fall Safety"
            },
                {
                    "osh_topic_id": 2,
                    "osh_topic_name": "Fall Safety"
                }],
            "Hardware_Options_for_ELT": [{
                "hardware_id": 1,
                "hardware_name": "Fall Safety"
            },
                {
                    "hardware_id": 2,
                    "hardware_name": "Fall Safety"
                }],
        }]
    }
