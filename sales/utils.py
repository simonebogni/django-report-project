import uuid, base64
from customers.models import Customer
from profiles.models import Profile
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns

def generate_transaction_id():
    code = str(uuid.uuid4()).replace('-', '').upper()[:12]
    return code

def get_salesman_from_id(id):
    salesman = Profile.objects.get(id=id)
    return salesman.user.username

def get_customer_from_id(id):
    customer = Customer.objects.get(id=id)
    return customer

# Create all the charts available in Matplotlib and Seaburn
def get_graph():
    # Create a buffer
    buffer = BytesIO()
    # Create the plot with the use of the BytesIO buffer as a file buffer
    plt.savefig(buffer, format='png')
    # Set the cursor to the beginning of the stream
    buffer.seek(0)
    # retrieve the content of the file
    image_png = buffer.getvalue()
    # Enconde the image/plot with base64, so that it can be embedded in the page
    graph = base64.b64encode(image_png)
    # Decode it to get a string representation of the image
    graph = graph.decode('utf-8')
    # Close the buffer to free the memory
    buffer.close()
    return graph

def get_chart(chart_type, data, **kwargs):
    # Switch the backend, which is a tool responsible to render the plots
    # In this case we are using the Anti-Grain Geography
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10, 4))
    if chart_type == '#1':
        # plt.bar(data['transaction_id'], data['price'])
        sns.barplot(x='transaction_id', y='price', data=data)
    elif chart_type == '#2':
        labels = kwargs.get('labels')
        plt.pie(data=data, x='price', labels=labels)
    elif chart_type == '#3':
        plt.plot(data['transaction_id'], data['price'], color='purple', marker='*', markersize=16, markerfacecolor='orange')
    else:
        print('failed to identify the chart type')
    # Adjust the size of the chart in response to the figsize
    plt.tight_layout()

    chart = get_graph()
    return chart